project = "pkgbuilder"
aurcat = "16"

task :default => [:help]

task :help do
    puts "Usage: rake [update/docs/docshtml/docszip]"
end

task :docshtml do
    sh "cd docs && sphinx-build -b dirhtml -d ./_build/doctrees . ./html"
end

task :docszip do
    sh "cd docs/html/ && zip -r ../docs-#{project}.zip ./*"
end

task :docs do
    Rake::Task[:docshtml].invoke
    Rake::Task[:docszip].invoke
end

task :update, :ver do |t, args|
    if args[:ver].to_s.chomp == ''
        puts "Version number?"
        version = STDIN.gets.chomp
    else
        version = args[:ver].chomp
    end
    date = Time.now.strftime('%Y-%m-%d')

    sh "sed \"s/version=.*/version='#{version}',/\" setup.py -i"
    sh "sed \"s/release = .*/release = '#{version}'/\" docs/conf.py -i"
    sh "sed \"s/:Version: .*/:Version: #{version}/\" docs/*.rst -i"
    sh "sed \"s/:Date: .*/:Date: #{date}/\" docs/*.rst -i"
    sh "rm docs/pkgbuilder.8.gz"
    sh "rst2man docs/pkgbuilder.rst > docs/pkgbuilder.8"
    sh "gzip docs/pkgbuilder.8"

    Rake::Task[:docs].invoke

    sh './setup.py sdist upload'
    md5sum = `md5sum "dist/#{project}-#{version}.tar.gz"`
    md5sum.chomp!
    md5sum.sub!("  dist/#{project}-#{version}.tar.gz", "")
    sh "sed \"s/md5sums=.*/md5sums=('#{md5sum}')/\" PKGBUILD -i"

    sh "tar -czvf /tmp/#{project}-#{version}-1.src.tar.gz PKGBUILD"
    sh "aurploader /tmp/#{project}-#{version}-1.src.tar.gz"

    puts "Done.  Please upload the docs tarball to PyPI."
end
