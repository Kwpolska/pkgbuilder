��    V      �     |      x     y     �     �     �  "   �     �     �  (   	  '   2     Z     j     �     �     �     �  5   �     	     <	     U	     s	     �	     �	  (   �	  #   �	     
     
     7
     C
     O
  R   W
      �
  ,   �
  !   �
  R        m     �     �     �     �  "   �          '  !   ,     N     W     e  ,   |  2   �     �  "   �  "        =  !   Q     s     �     �  2   �     �     �  
   �  	   �  
             "     *     ?  #   N     r     �     �  +   �     �       �             *  9   0  9   j  1   �     �     �     �                +  �  =     �     �     �     �          "  !   3  +   U  ,   �     �     �     �     �       !     C   =  !   �     �  !   �      �     �        -   ;  &   i     �     �     �     �     �  _   �  %   4  9   Z  "   �  c   �          ;     M  /   l     �  +   �     �     �  %   �                /  2   P  A   �     �  &   �  1        8  +   R     ~     �     �  2   �     �               #     3     ?     T     ]     t     �  #   �  !   �     �  @     #   D     h    l     |     �  E   �  8   �  5        S     W     i     }     �     �     P          S   8      )   +   '      "          I   >       &          U                  $      D          E   K   %                       !   -   O           N   ;          4              F      C   .   M                           *   
   /       0   Q   1   R           5   7       G       	   #   9              H           ?   6                <   :          ,   3          B             (          =              T             2   V               L   J          A   @     [installed: {0}]  [installed] %(prog)s <operation> [...] (dummy) :: Retrieving packages from aur... AUR Error: {0} Aborted by user! Exiting... An AUR helper (and library) in Python 3. Building more AUR packages is required. Building {0}... Checking dependencies... Connection error: {0} (via {1}) Didn’t pass any packages. ERROR: Error while processing {0}: {1} Failed to fulfill package dependency requirement: {0} Fetching package information... HTTP Error {0} (via {1}) Initializing pacman access... Installing built packages... Installing with pacman -U... Interrupt signal received
 LANG locale by AUTHOR <MAIL@IF.YOU.WANT> Moving to /var/cache/pacman/pkg/... Name Network error: {0} (via {1}) New Version Old Version PACKAGE PKGBUILDer (or the requests library) had problems with fulfilling an HTTP request. Package {0} not found. (via {1}) Please restart PKGBUILDer as a regular user. Proceed with installation? [Y/n]  Running as root is not allowed as it can cause catastrophic damage to your system! Sanity error!  {0} (via {1}) Search query too short Searching for exact match... Starting full system upgrade... Successfully fetched:  Synchronizing package databases... Targets ({0}): USER Validating installation status... WARNING: [out of date] display debug messages don't check dependencies (may break makepkg) don't check if packages were installed after build don't use colors in output error: package '{0}' was not found fetch all package files of an user fetch package files found an existing package for {0} found in repos found in system found in the AUR makepkg (or someone else) failed and returned {0}. makepkg returned {0}. no none found not found operations optional arguments options positional arguments retrieving {0} search the AUR for matching strings show this help message and exit show version number and quit there is nothing to do upgrade all the VCS/date-versioned packages upgrade installed AUR packages usage usage:  {0} <operation> [...]

PBWrapper, a wrapper for pacman and PKGBUILDer.

{1}

Pacman and PKGBUILDer syntaxes apply.  Consult their manpages/help
commands for more details.

Additional options:
  -L, --unlock         unlock the pacman database view package information votes warning: insufficient columns available for table display warning: {0}: downgrading from version {1} to version {2} warning: {0}: local ({1}) is newer than aur ({2}) yes {0} (Package: {1}) {0}: NOT installed {0}: installed {1} {0}: not an AUR package {0}: outdated {1} Project-Id-Version: 4.3.2
Report-Msgid-Bugs-To: Chris Warrick <chris@chriswarrick.com>
PO-Revision-Date: 2019-01-12 14:40+0000
Last-Translator: Chris Warrick
Language-Team: Portuguese (http://www.transifex.com/kwpolska/pkgbuilder/language/pt/)
Language: pt
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=(n != 1);
 [instalado: {0}] [instalado] %(prog)s <operação> [...] (dummy) :: Obtendo pacotes do aur... Erro do AUR: {0} Abortado pelo usuário! Saindo... Uma biblioteca e helper do AUR em Python 3. É necessário compilar mais pacotes do AUR. Construindo {0}... Checando dependências.. Erro de conexão: {0} (via {1}) Não passou pacote nenhum. ERRO: Erro enquanto processava {0}: {1} Falhou para satisfazer os requisitos de dependência do pacote: {0} Obtendo informações do pacote.. Erro HTTP {0} (via {1}) Inicializando acesso do pacman... Instalando pacotes compilados... Instalando com pacman -U... Sinal de interrupção recebido
 Locale LANG pelo AUTOR <email@se.voce.quiser> Movendo para /var/cache/pacman/pkg/... Nome Erro de rede: {0} (via {1}) Nova Versão Versão antiga PACOTE PKGBUILDer (ou a biblioteca de requisição) teve problemas para realizar uma requisição HTTP Pacote {0} não encontrado. (via {1}) Por favor reinicie o PKGBUILDer como um usuário regular. Proceder com a instalação? [S/n] Rodar como root não é permitido já que isso pode causar danos catastróficos para o seu sistema! Erro de sanidade! {0} (via {1}) Busca muito curta Procurando pela busca exata... Começando atualização completa do sistema... Baixou com sucesso: Sincronizando bancos de dados de pacotes... Alvos ({0}): USUÁRIO Validando o estado da instalação... AVISO: [desatualizado] mostrar mensagens de depuração não checar dependências (pode quebrar o makepkg) não checar se os pacotes foram instalados depois da compilação não usar cores na saída erro: pacote '{0}' não foi encontrado baixar todos os arquivos do pacote de um usuário baixar arquivos do pacote um pacote existente para {0} foi encontrado encontrado nos repositórios encontrado no sistema encontrado no AUR makepkg (ou outro programa) falhou e retornou {0}. makepkg retornou {0}. não nenhum encontrado não encontrado operações argumentos opcionais opções argumentos posicionais recebendo {0} procurar essas strings no AUR mostra essa mensagem de ajuda e sai mostrar número da versão e sair não há nada para ser feito atualizar todos os pacotes de VCS ou versionados com alguma data atualizar pacotes instalados do AUR uso uso:  {0} <operação> [...]

PBWrapper, um wrapper para o pacman e para o PKGBUILDer.

{1}

Sintaxes do Pacman e do PKGBUILDer se aplicam.  Consulte seus manuais para mais detalhes.

Opções adicionais:
  -L, --desbloquear         desbloquear o banco de dados do pacman ver informações do pacote votos aviso: colunas disponíveis são insuficientes para display de tabela aviso: {0}: rebaixando da versão {1} para a versão {2} aviso: {0}: local ({1}) é mais novo do que aur ({2}) sim {0} (Pacote: {1}) {0}: NÃO instalado {0}: instalado {1} {0}: não é um pacote do AUR {0}: desatualizado {1} 