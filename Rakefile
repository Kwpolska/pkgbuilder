project = "pkgbuilder"
aurcat = "16"

task :default => [:help]

task :help do
    puts "Usage: rake command"
    puts "Command is one of:"
    puts "  update    Updates the package."
    puts "  docs      Creates the docs."
    puts ""
    puts "  prepare   Prepares the package for being updated."
    puts "  pypi      Creates and uploads the package to pypi."
    puts "  aur       Uploads an AUR tarball."
    puts "  docshtml  Creates the docs in HTML."
    puts "  docszip   Zips the docs made by docshtml."

end

task :prepare, :ver do |t, args|
    if args[:ver].to_s.chomp == ''
        puts "Version number?"
        version = STDIN.gets.chomp
    else
        version = args[:ver].chomp
    end

    date = Time.now.strftime('%Y-%m-%d')

    sh "sed \"s/version=.*/version='#{version}',/\" setup.py -i"
    sh "sed \"s/release = .*/release = '#{version}'/\" docs/conf.py -i"
    sh "sed \"s/version = .*/version = '#{version}'/\" docs/conf.py -i"
    sh "sed \"s/:Version: .*/:Version: #{version}/\" docs/*.rst -i"
    sh "sed \"s/:Version: .*/:Version: #{version}/\" README.rst -i"
    sh "sed \"s/BUILDer .* do/BUILDer #{version} do/\" docs/index.rst -i"
    sh "sed \"s/# PKG.*/# PKGBUILDer v#{version}/\" pkgbuilder.py -i"
    sh "sed \"s/VERSION = .*/VERSION = '#{version}'/\" pkgbuilder.py -i"
    sh "sed \"s/pkgver=.*/pkgver=#{version}/\" PKGBUILD -i"

    sh "sed \"s/:Date: .*/:Date: #{date}/\" docs/*.rst -i"
    sh "sed \"s/:Date: .*/:Date: #{date}/\" README.rst -i"
end

task :docshtml do
    sh "cd docs && sphinx-build -b dirhtml -d ./_build/doctrees . ./html"
end

task :docszip do
    sh "cd docs/html/ && zip -r ../docs-#{project}.zip ./*"
end

task :docs do
    sh "rm docs/pkgbuilder.8.gz"
    sh "rst2man docs/pkgbuilder.rst > docs/pkgbuilder.8"
    sh "gzip docs/pkgbuilder.8"

    #Rake::Task[:docshtml].invoke
    #Rake::Task[:docszip].invoke
end

task :pypi do
    sh './setup.py sdist upload'
end

task :aur, :ver do |t, args|
    if args[:ver].to_s.chomp == ''
        puts "Version number?"
        version = STDIN.gets.chomp
    else
        version = args[:ver].chomp
    end

    pbdir = "/tmp/#{project}-pkgbuild-#{version}"
    sh "mkdir -p #{pbdir}"
    sh "cp PKGBUILD #{pbdir}"
    md5out = `cd #{pbdir} && makepkg -cg`
    md5sums = md5out.split('\n').reverse[0].chomp!
    sh "sed \"s/md5sums=.*/#{md5sums}/\" PKGBUILD -i"
    sh "cp PKGBUILD #{pbdir}"
    sh "cd #{pbdir} && makepkg -f --source"
    sh "aurupload Kwpolska - system #{pbdir}/*.src.tar.gz"


end

task :git, :ver, :msg do |t, args|
    if args[:ver].to_s.chomp == ''
        puts "Version number?"
        version = STDIN.gets.chomp
    else
        version = args[:ver].chomp
    end

    if args[:msg].to_s.chomp == ''
        puts "Commit message (sans the version)?"
        commitmsg = STDIN.gets.chomp
    else
        commitmsg = args[:msg].chomp
    end

    sh "git add *"
    sh "git commit -asm 'v#{version}: #{commitmsg}'"
    sh "git tag -a 'v#{version}' -m 'Version #{version}'"
    sh "git push --tags"
end

task :update, :ver do |t, args|
    if args[:ver].to_s.chomp == ''
        puts "Version number?"
        version = STDIN.gets.chomp
    else
        version = args[:ver].chomp
    end
    #date = Time.now.strftime('%Y-%m-%d')

    Rake::Task[:prepare].invoke(version)

    Rake::Task[:docs].invoke(version)

    Rake::Task[:pypi].invoke(version)

    Rake::Task[:aur].invoke(version)

    Rake::Task[:git].invoke(version, '')

    puts "Done everything.  Bye."
end
