---
title: "ITA_Samsung Drive Manager FAQ Ver 2.5.pdf"
source_file: "硬盘驱动文件\Samsung Drive Manager Manuals\Italian\ITA_Samsung Drive Manager FAQ Ver 2.5.pdf"
type: 全量文档抽取
ext: ".pdf"
size_mb: "0.074"
modified: "2012-06-27"
is_backup: "否"
char_count: 11326
---

# 原文抽取：ITA_Samsung Drive Manager FAQ Ver 2.5.pdf

> 来源路径：`硬盘驱动文件\Samsung Drive Manager Manuals\Italian\ITA_Samsung Drive Manager FAQ Ver 2.5.pdf` ｜ 类型：.pdf ｜ 大小：0.074MB ｜ 修改：2012-06-27 ｜ 备份：否

```text
Domande frequenti su Samsung
Drive Manager

Installazione
D: Il disco fisso esterno Samsung è collegato, ma non succede nulla.
R: Verificare la connessione del cavo USB. Se il disco fisso esterno Samsung è collegato correttamente, il LED del disco si accende.
R. Se dal disco fisso proviene un ticchettio, l'alimentazione è insufficiente. Se con la porta USB corrente il disco fisso non viene riconosciuto, provare a connetterlo a un'altra porta USB.
D. Non riesco a installare Samsung Drive Manager.
R: Verificare che il sistema soddisfi i requisiti minimi per l'uso di un disco fisso esterno Samsung. Per ulteriori informazioni, fare riferimento alle specifiche di sistema illustrate nel Capitolo 1 del Manuale per l'utente.)
D. Quando eseguo Samsung Drive Manager in Windows Vista continua a essere visualizzata la finestra "Controllo dell'account utente". Come devo procedere per far sìche la finestra non venga più visualizzata?
R. Per utilizzare Samsung Drive Manager per accedere direttamente o indirettamente a un disco fisso esterno è necessaria l'elevazione dei privilegi. L'uso di Samsung Drive Manager è limitato se l'accesso mediante il controllo dell'account utente non è autorizzato. Per evitare la visualizzazione della finestra "Controllo dell'account utente",

selezionare Account utente nel pannello di controllo e disattivare l'opzione Attiva o disattiva Controllo account utente.

Samsung AutoBackup
D: Di quali elementi è necessario eseguire il backup?
R. In generale, è necessario eseguire il backup dei file di dati generati mediante l'uso delle applicazioni. Non è utile eseguire il backup dei file di programma, perché se dovesse verificarsi un problema nel computer i programmi dovrebbero comunque essere reinstallati. È consigliabile eseguire il backup dei file di dati che è possibile ripristinare.
D. Con che frequenza è opportuno eseguire il backup dei dati?
R. Se il backup non viene eseguito regolarmente, è consigliabile eseguire il backup dei file importanti e dei dati personali, come le foto, che non è possibile o è difficile ricreare.
D. Alcuni file sono stati modificati, ma il backup in tempo reale non è stato eseguito.
R. Se viene modificato un file che non è impostato come origine per il backup, Samsung AutoBackup non esegue il backup in tempo reale. Assicurarsi di avere impostato per il backup in tempo reale i tipi di file desiderati.
R. Un'altra possibile causa è che una cartella o un file del sistema operativo sia stato incluso in un'origine di backup. Non è possibile eseguire il backup di questi file con Samsung AutoBackup, perché sono utilizzati dal sistema.

Controllare che le cartelle o i file del sistema operativo non vengano inclusi nelle origini dei backup.
D. Utilizzo Samsung AutoBackup in Windows Vista o Windows 7 e i dati e i registri di backup non vengono visualizzati.
R. Questo problema è causato dalla funzione Controllo dell'account utente introdotta con Windows Vista.
Un disco fisso formattato come NTFS in Windows XP non dispone dell'autorizzazione
(Utenti autenticati) concessa con la formattazione in Windows Vista o Windows 7. Se un disco fisso privo di questa autorizzazione viene connesso a Windows Vista o Windows 7 e utilizzato, i dati di backup non vengono aggiornati normalmente.
※ FAT32 non risente di questo problema.
D. Sebbene lo spazio disponibile nel mio disco fisso esterno Samsung sia sufficiente, non riesco a eseguire il backup di file più grandi di 2 GB o 4 GB.
R. La dimensione massima dei file di cui è possibile eseguire il backup dipende dal file system del disco fisso esterno Samsung.
Tabella 1: File system

Tipo di file system FAT
FAT32 NTFS

Dimensione massima dei file di backup
2 GB
4 GB
16 TB

R. Per eseguire il backup di un file di dimensioni superiori a 2 GB, è necessario cambiare il file system in FAT32 o NTFS. Per eseguire il backup di un file di dimensioni superiori a 4 GB, è necessario cambiare il file system in NTFS.
NOTA: SE SI CAMBIA IL FILE SYSTEM, TUTTI I DATI MEMORIZZATI NEL DISCO FISSO ESTERNO SAMSUNG
VENGONO ELIMINATI. PRIMA DI CAMBIARE IL FILE SYSTEM, ESEGUIRE IL BACKUP DI TUTTI I DATI IMPORTANTI IN UN ALTRO DISCO FISSO.

D. Ho formattato il computer e reinstallato Windows. Come posso ripristinare i dati di backup in un altro dispositivo?
R. Installare Samsung Drive Manager ed eseguire Samsung AutoBackup, quindi selezionare dall'elenco dei processi i dati da ripristinare. I dati di backup possono essere utilizzati in questo modo (per ulteriori informazioni, fare riferimento al Capitolo 2 del Manuale per l'utente).

D. Dopo la mancata riuscita di un backup, ho controllato il registro di backup e ho constatato che si erano verificati diversi errori.
R. Non è possibile accedere ai file del sistema operativo per eseguirne il backup. Non è possibile eseguire il backup dei file del sistema operativo. Questo problema si verifica frequentemente quando una cartella di Windows o una cartella contenente file di programma viene impostata come origine per il backup. Per evitarlo, non impostare un'intera cartella principale come origine per il backup, ma solo le cartelle degli utenti.
R. Un altro modo per evitare il problema è escludere dall'origine di backup i file che provocano l'errore ed eseguire nuovamente il backup.
D: Ho formattato il disco fisso esterno Samsung e il software Samsung che conteneva è stato eliminato.
R. Il software Samsung fornito con il disco fisso esterno Samsung può essere scaricato dal sito Web dell'assistenza clienti Samsung. (http://www.samsung.com/sec)
D. Ho eseguito il backup di un programma che era stato installato insieme a un prodotto. Nel prodotto si è verificato un problema, pertanto ho eliminato il programma e ho ripristinato il file di cui avevo eseguito il backup, ma non riesco a eseguire il prodotto. Ho sbagliato qualcosa nella procedura di backup e ripristino?
R. L'esecuzione di tutti i programmi software richiede un determinato ambiente. Quando si installa un programma in un computer, insieme ai file del programma viene installato

un ambiente; quando si esegue il programma l'ambiente installato viene verificato. Poiché Samsung AutoBackup non esegue il backup dell'ambiente, non è possibile eseguire il programma anche se viene ripristinato dopo che ne è stato eseguito il backup.
D: Quando Samsung AutoBackup è in esecuzione non riesco a rimuovere il disco fisso esterno Samsung con la funzione "Rimozione sicura dell'hardware".
R. Non è possibile rimuovere il disco fisso esterno Samsung mentre è in uso. Riprovare dopo aver chiuso Samsung AutoBackup.
D: I trasferimenti dei file richiedono troppo tempo.
R. Se il computer non supporta USB 2.0 o 3.0 o se il disco fisso esterno Samsung è connesso a una porta diversa da USB 2.0 o 3.0, la velocità di trasferimento dei file si riduce. Connettere il disco fisso esterno Samsung a una porta che supporti USB 2.0 o una versione successiva.
D. Non riesco a copiare i file del mio computer Macintosh.
R. La compatibilità dei file system può rappresentare un problema. Se il disco fisso esterno Samsung è formattato come NTFS, i dati salvati possono essere letti solo in un sistema Macintosh.

D: Quando controllo i miei file di backup nel dispositivo di backup, viene visualizzato un messaggio che afferma che il file non è nel formato corretto, e i file risultano illeggibili.
R. Se nelle impostazioni di backup è stata selezionata l'opzione Backup crittograf., i file vengono crittografati e quindi ne viene eseguito il backup. Quando si apre un file crittografato si verifica un errore o viene visualizzato un messaggio che afferma che il file non è nel formato corretto. Per poter aprire un file crittografato è necessario prima ripristinarlo.
D. Ho eseguito un backup con l'opzione "Crittografia" attivata. Ma sono stati crittografati solo alcuni file.
R. Solo i file di cui si esegue il backup dopo aver attivato la crittografia vengono crittografati. I file di cui è stato eseguito il backup prima di attivare l'opzione Crittografia non vengono crittografati. Ciò significa che nello stesso dispositivo di backup possono essere presenti file crittografati e non crittografati.
D: Posso connettere un disco fisso esterno Samsung che contiene dati di backup provenienti da un altro computer e ripristinare questi dati? E, in caso affermativo, in che modo?
R. Per ripristinare e utilizzare i dati di backup provenienti da un altro computer, connettere il disco fisso esterno Samsung al computer e installare Samsung Drive Manager, quindi

eseguire Samsung Auto Backup e selezionare i file di backup da ripristinare.
D: Come posso controllare i risultati di backup, ripristini o eliminazioni?
R. Dopo il completamento del backup, del ripristino o dell'eliminazione è possibile visualizzare i risultati in "Registro", nel menu del processo della schermata Samsung AutoBackup.

Samsung SecretZone
D: Come posso proteggere la mia unità protetta dagli altri utenti?
R: Selezionare un'immagine da proteggere in Samsung SecretZone, quindi selezionare "Disconnetti." Gli altri utenti non potranno visualizzare l'unità protetta finché l'amministratore non selezionerà "Connetti".
D: Come posso usare nuovamente l'unità protetta dopo avere reinstallato il sistema operativo?
R: Per riutilizzare l'unità protetta dopo avere reinstallato il sistema operativo, reinstallare Samsung Drive Manager, connettere il disco fisso esterno Samsung, selezionare l'unità protetta da utilizzare in Samsung SecretZone e fare clic su "Connetti."
D: Qual è la dimensione massima di un'unità protetta?
R: La dimensione di un'unità protetta può corrispondere allo spazio libero nel disco fisso esterno Samsung.
D: Che posso fare se dimentico la password?

R: Samsung SecretZone è un programma di protezione e non è possibile utilizzare l'unità protetta senza la password corretta. Assicurarsi che la password impostata per l'unità protetta sia semplice da ricordare.
D: Mentre Samsung SecretZone è in esecuzione, non riesco a rimuovere il disco fisso esterno Samsung con la funzione Rimozione sicura dell'hardware.
R: Disconnettere tutte le unità protette in esecuzione, chiudere Samsung SecretZone e quindi procedere alla rimozione sicura del disco fisso esterno Samsung.

D: Dopo l'attivazione dell'opzione "Connessione automatica", l'unità protetta non si connette.
R: A seconda delle specifiche del PC, la connessione del disco fisso esterno Samsung può richiedere del tempo. Attendere finché la connessione viene stabilita.
D: Quando disconnetto l'unità protetta viene visualizzato un messaggio di errore.
R: Se l'unità protetta viene disconnessa immediatamente dopo la copia e il salvataggio di un file di grandi dimensioni o di più file, può verificarsi un errore. In questo caso, attendere da 30 secondi a 1 minuto e riprovare.

Samsung Secure Manager
D: Posso sbloccare il disco fisso protetto Samsung senza installare Samsung Drive Manager?
R: Connettere il disco fisso protetto Samsung, eseguire Secure Unlocker_win.exe nell'unità CD visualizzata in "Risorse del computer" e immettere la password di sblocco.
A. Secure Unlock_mac.app deve essere eseguito in Macintosh.
D: Che cos'è la funzione Impostazioni fabbrica?
R: La funzione Impostazioni fabbrica consente di eliminare tutti i dati memorizzati nel disco fisso protetto e ripristinare le impostazioni di protezione predefinite.
```
