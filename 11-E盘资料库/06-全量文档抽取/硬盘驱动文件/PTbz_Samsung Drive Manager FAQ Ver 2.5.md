---
title: "PTbz_Samsung Drive Manager FAQ Ver 2.5.pdf"
source_file: "硬盘驱动文件\Samsung Drive Manager Manuals\Portuguese (Brazlian)\PTbz_Samsung Drive Manager FAQ Ver 2.5.pdf"
type: 全量文档抽取
ext: ".pdf"
size_mb: "0.074"
modified: "2012-06-27"
is_backup: "否"
char_count: 10802
---

# 原文抽取：PTbz_Samsung Drive Manager FAQ Ver 2.5.pdf

> 来源路径：`硬盘驱动文件\Samsung Drive Manager Manuals\Portuguese (Brazlian)\PTbz_Samsung Drive Manager FAQ Ver 2.5.pdf` ｜ 类型：.pdf ｜ 大小：0.074MB ｜ 修改：2012-06-27 ｜ 备份：否

```text
Perguntas frequentes do Samsung Drive
Manager

Instalação
P: Meu Disco Rígido Externo Samsung está conectado, mas nada está acontecendo.
R: Verifique a conexão a cabo USB. Se seu Disco Rígido Externo Samsung está conectado adequadamente, seu LED deverá estar aceso.
A. Um ruído de tique-taque no disco rígido significa que a fonte de alimentação não está fornecendo energia suficiente. Se o disco rígido não for reconhecido na porta USB atual, tente conectá-lo a outra porta USB.
P. Não consigo instalar o Samsung Drive Manager.
R: Verifique os requisitos mínimos do sistema para usar o Disco Rígido Externo Samsung. Consulte as Especificações do Sistema no Capítulo 1 do Manual do Usuário para obter mais informações.
P. A janela "Controle da conta do usuário" continua aparecendo quando executo o Samsung Drive Manager no Windows Vista. Como eu posso fazer parar de aparecer a janela "Controle da conta do usuário"?
A. É necessário a Elevação para usar o Samsung Drive Manager para acessar direta ou indiretamente um disco rígido externo. O uso do Samsung Drive Manager é restrito se o acesso para "Controle da conta do usuário" não está autorizado. Para impedir a exibição da janela "Controle da

conta do usuário", selecione a Conta do usuário no Painel de controle e defina Desativar controle da conta do usuário.

Samsung AutoBackup
P: Do que eu devo fazer backup?
P. Em geral, deve ser feito backup dos arquivos de dados gerados pelo uso de outro software. Não é recomendado fazer backup de arquivos de programas, os programas devem ser instalados novamente se seu computador enfrentar um problema. Recomenda-se o backup de arquivos de dados que podem ser restaurados.
P. Com que frequência eu devo fazer backup de dados?
R. Se você não fizer backup regularmente, recomenda-se que faça backup de arquivos importantes, dados pessoais como fotografias e arquivos que não podem ser criados novamente ou que são difíceis de criar.
P. Alguns arquivos foram alterados, mas o backup em tempo real não foi executado.
R. O Samsung AutoBackup não pode executar o backup em tempo real se um arquivo não definido como origem do backup for alterado. Certifique-se de que os tipos de arquivo, dos quais você deseja fazer backup em tempo real, estejam definidos para backup em tempo real.
R. Outra causa é um arquivo ou pasta do sistema OS sendo incluído em uma origem de backup. O Samsung AutoBackup não pode fazer backup de arquivos enquanto eles são usados pelo sistema. Certifique-se de que pastas

ou arquivos do sistema OS não estejam incluídos como uma origem de backup.
P. Eu uso o Samsung AutoBackup no Windows Vista ou no Windows 7 e os dados com backup e os logs de backup não são exibidos.
R. Este problema é causado pela função User Account Control introduzida na liberação do Windows Vista.
R. Um HDD formatado como NTFS no Windows XP não tem direitos
(Authenticated Users) concedidos quando formatado no Windows Vista ou no Windows 7. Se um HDD sem estes direitos for conectado ao Windows Vista ou Windows 7 e usado, os dados de backup não serão atualizados normalmente.
※ FAT32 não é afetado por este problema.
P. Eu tenho espaço suficiente no meu Disco Rígido Externo Samsung, mas não posso fazer backup de arquivos maiores de 2 ou 4 GB.
R. O tamanho máximo de arquivo do qual pode ser feito backup depende do sistema de arquivos do Disco Rígido Externo Samsung.
Tabela 1: Sistema de arquivos

Tipo do sistema de arquivos
FAT
FAT32
NTFS

Tamanho máximo do arquivo de backup
2 GB
4 GB
16 TB

P. Para fazer backup de um arquivo maior de 2 GB, o sistema de arquivos deve ser alterado para FAT32 ou NTFS. Para fazer backup de um arquivo maior de 4 GB, o sistema de arquivos deve ser alterado para NTFS.
OBSERVAÇ Ã O: TODOS OS DADOS ARMAZENADOS NO DISCO RÍGIDO EXTERNO SAMSUNG SERÃ O EXCLUÍDOS
SE O SISTEMA DE ARQUIVOS FOR ALTERADO. FAÇ A BACKUP DE TODOS OS DADOS IMPORTANTES PARA OUTRO DISCO RÍGIDO ANTES DE ALTERAR O SISTEMA
DE ARQUIVOS.

P. Eu formatei meu computador e instalei novamente o Windows. Como posso restaurar meus dados de backup em outro dispositivo?
R. Instalar o Samsung Drive Manager e executar o Samsung AutoBackup e a seguir selecionar os dados para restauração na Lista de trabalho. O dados de backup podem ser usados desta maneira (consulte o Capítulo 2 do Manual do Usuário para obter informações adicionais). )

P. Após uma falha no backup, verifiquei o log do backup e vi que ocorreram várias falhas de backup.
R. Os arquivos do sistema OS não podem ser acessados para fazer backup. Os arquivos do sistema OS não podem ser submetidos a backup. Este problema é experimentado normalmente quando uma pasta Windows ou uma pasta "Arquivos de programas" é definida como uma origem de backup. Para evitar este problema, não defina uma pasta raiz inteira como a origem do backup. Defina somente pastas de usuários como origem de backup.
R. Outra maneira de evitar este problema é excluir o arquivo com falha como origem de backup, e executar o backup novamente.
P: Eu formatei o Disco Rígido Externo Samsung e o software Samsung presente no disco foi excluído.
R. O software Samsung fornecido com o Disco Rígido Externo Samsung pode ser baixado do site de suporte ao cliente Samsung. (http://www.samsung.com/sec)
P. Eu fiz backup de um programa que estava instalado quando instalei um produto. O produto apresentou um problema, por isso, eu exclui o programa e restaurei o arquivo de backup, mas não fui capaz de executar o produto. Eu fiz alguma coisa errada no processo de backup e restauração?
R. Todos os programas de software exigem um certo ambiente para ser executado. Quando um programa é instalado em um computador, um ambiente é instalado junto com os arquivos de programa e quando o programa é executado, o

ambiente instalado é testado. Como o Samsung AutoBackup não faz backup de um ambiente assim, este programa não pode ser executado nem mesmo após ser feito o backup e a restauração.
P: Quando o Samsung AutoBackup está em execução, eu não posso remover o Disco Rígido Externo Samsung usando a função "Remover hardware com segurança".
R. O Disco Rígido Externo Samsung não pode ser removido com segurança enquanto estiver em uso. Tente novamente após fechar o Samsung AutoBackup.
P: A transferência do arquivo está demorando muito.
R. Se o seu computador não suporta USB 2.0 ou 3.0 ou se seu Disco Rígido Externo Samsung está conectado a uma porta diferente de uma porta USB 2.0 ou 3.0, a velocidade de transferência de arquivos é reduzida. Conecte seu Disco Rígido Externo Samsung a uma porta que suporta USB 2.0 ou superior.
Q. Eu não consegui copiar arquivos no meu computador Macintosh.
R. A compatibilidade do sistema de arquivos pode ser um problema. Se o Disco Rígido Externo Samsung estiver formatado como NTFS, os dados salvos só poderão ser lidos em um sistema Macintosh.

P: Quando eu verifico meus arquivos de backup no dispositivo de backup, vejo uma mensagem que diz: "O arquivo não está no formato adequado" e arquivos ilegíveis.
P. Se Backup criptogr. tiver sido selecionado nas configurações de backup, os arquivos serão criptografados e o backup executado. Quando um arquivo criptografado é aberto, ocorre um erro ou é exibida uma mensagem que diz: "O arquivo não está no formato adequado". Um arquivo criptografado deve ser, primeiro, restaurado antes de ser aberto.
P. Eu executei um backup com a opção "Criptografia" habilitada. Mas somente os arquivos selecionados foram criptografados.
P. Após a habilitação da opção Criptografar, somente os arquivos com backup serão habilitados, criptografados e o backup executado. Antes da habilitação da opção Criptografar, os arquivos com backup não haviam sido criptografados. Isto significa que os arquivos criptografados e os não criptografados podem existir no mesmo dispositivo de backup.
P: Eu posso conectar o Disco Rígido Externo Samsung contendo dados de backup de outro computador e restaurar os dados de backup? Se for possível, como posso fazer isso?

R. Para restaurar e usar dados de backup de outro computador, conecte seu Disco Rígido Externo Samsung ao computador e instale o Samsung Drive Manager, depois, execute o Samsung Auto Backup, e selecione o arquivo de backup para restaurar.
P: Como posso verificar os resultados do backup, da restauração ou da exclusão ?
R. Após o backup, a restauração ou a exclusão estará concluída, você pode ver o resultado no "Log" mostrado no menu de trabalho na tela Samsung AutoBackup.

Samsung SecretZone
P: Como posso proteger minha Unidade segura de outros usuários?
R: Selecione uma imagem para proteger no Samsung SecretZone e selecione "Desconectar." Outros usuários não poderão ver a Unidade segura até que "Conectar" seja selecionada pelo administrador.
P: Como posso usar minha Unidade segura novamente apó s reinstalar o OS?
R: Para usar sua Unidade segura novamente após reinstalar o OS, reinstale o Samsung Drive Manager, conecte o Disco Rígido Externo Samsung, selecione a Unidade segura para usar em Samsung SecretZone e clique em "Conectar."
P: Qual é o tamanho máximo da Unidade segura ?
R: O tamanho de uma Unidade segura pode ser tão grande quanto o espaço livre no Disco Rígido Externo Samsung.
P: O que devo fazer se eu esquecer a senha?

R: O Samsung SecretZone é um programa de segurança e sua Unidade segura não pode ser usada sem a senha correta. Certifique-se de que a senha que definiu para a Unidade segura é uma senha que você pode se lembrar facilmente.
P: Enquanto o Samsung SecretZone está em execução, não posso remover o Disco Rígido Externo Samsung usando a função Remover hardware com segurança.
R: Desconecte todas as Unidades seguras em execução, feche o Samsung SecretZone e, a seguir, remova o Disco Rígido Externo Samsung.

P: Apó s habilitar "Conexão automática" na minha Unidade segura, ela não se conecta.
R: Dependendo das especificações do seu PC, ele pode levar algum tempo para conectar o Disco Rígido Externo Samsung. Espere um momento até que a conexão seja estabelecida.
P: Uma mensagem de erro é exibida quando desconecto minha Unidade segura.
R: Pode ocorrer um erro quando sua Unidade segura é desconectada, imediatamente após copiar ou salvar um arquivo grande ou vários arquivos. Se ocorrer um erro, tente novamente após 30 segundos a 1 minuto.

Samsung Secure Manager
P: Posso desbloquear o Disco Rígido Seguro Samsung sem instalar o Samsung Drive Manager?
R: Conecte o Disco Rígido Seguro Samsung, execute o Secure Unlocker_win.exe na unidade CD exibida em "Meu computador" e, depois, digite a senha para desbloquear.
A. O Secure Unlock_mac.app deve ser executado no Macintosh.
P: O que é a função Redefinição de padrão de fábrica?
R: A função Redefinição de padrão de fábrica exclui todos os dados salvos no Disco Rígido Seguro, e restaura as configurações de segurança padrão.
```
