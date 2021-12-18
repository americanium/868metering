#!/usr/bin/perl


# Einbinden der LoxBerry-Module
use CGI;
use LoxBerry::System;
use LoxBerry::Web;
  
# Die Version des Plugins wird direkt aus der Plugin-Datenbank gelesen.
my $version = LoxBerry::System::pluginversion();
 
# Mit dieser Konstruktion lesen wir uns alle POST-Parameter in den Namespace R.
my $cgi = CGI->new;
$cgi->import_names('R');
# Ab jetzt kann beispielsweise ein POST-Parameter 'form' ausgelesen werden mit $R::form.
 
 
# Wir Übergeben die Titelzeile (mit Versionsnummer), einen Link ins Wiki und das Hilfe-Template.
# Um die Sprache der Hilfe brauchen wir uns im Code nicht weiter zu kümmern.
LoxBerry::Web::lbheader("Sample Plugin for Perl V$version", "http://www.loxwiki.eu/x/2wN7AQ", "help.html");
  
# Wir holen uns die Plugin-Config in den Hash %pcfg. Damit kannst du die Parameter mit $pcfg{'Section.Label'} direkt auslesen.
#my %pcfg;
#tie %pcfg, "Config::Simple", "$lbpconfigdir/pluginconfig.cfg";
my $pcfg = new Config::Simple("$lbpconfigdir/miflora.cfg");


# Wir initialisieren unser Template. Der Pfad zum Templateverzeichnis steht in der globalen Variable $lbptemplatedir.

my $template = HTML::Template->new(
    filename => "$lbptemplatedir/index.html",
    global_vars => 1,
    loop_context_vars => 1,
    die_on_bad_params => 0,
	associate => $cgi,
);
  
# Jetzt lassen wir uns die Sprachphrasen lesen. Ohne Pfadangabe wird im Ordner lang nach language_de.ini, language_en.ini usw. gesucht.
# Wir kümmern uns im Code nicht weiter darum, welche Sprache nun zu lesen wäre.
# Mit der Routine wird die Sprache direkt ins Template übernommen. Sollten wir trotzdem im Code eine brauchen, bekommen
# wir auch noch einen Hash zurück.
my %L = LoxBerry::Web::readlanguage($template, "language.ini");
  
my $lastdata;

# ---------------------------------------------------
# Save settings to config file
# ---------------------------------------------------
if ($R::btnSave)
{
	$pcfg->param('MIFLORA.MQTTSERVERIP', $R::txtMQTTServerIP);
	$pcfg->param('MIFLORA.MQTTSERVERPORT', $R::txtMQTTServerPort);
	$pcfg->param('MIFLORA.MQTTSERVERTOPIC', $R::txtMQTTServerTopic);
	$pcfg->param('MIFLORA.USBDEVICE', $R::txtUSBDevice);

	$pcfg->save();
	
	open(my $DATEIHANDLER, ">$lbptemplatedir/wmbusmeters.conf");
	print $DATEIHANDLER "loglevel=normal\n";
	print $DATEIHANDLER "device=$R::txtUSBDevice\n";
	print $DATEIHANDLER "logtelegrams=true\n";
	print $DATEIHANDLER "format=json\n";
	print $DATEIHANDLER "meterfiles=/var/log/wmbusmeters/meter_readings\n";
	print $DATEIHANDLER "meterfilesaction=overwrite\n";
	print $DATEIHANDLER "meterfilesnaming=name\n";
	print $DATEIHANDLER "meterfilestimestamp=hour\n";
	print $DATEIHANDLER "logfile=/var/log/wmbusmeters/wmbusmeters.log\n";
	
	print $DATEIHANDLER "shell=/usr/bin/mosquitto_pub -h $R::txtMQTTServerIP -p $R::txtMQTTServerPort -u $R::txtMQTTServerUsername -P $R::txtMQTTServerPassword -t $R::txtMQTTServerTopic -m " . '"$METER_JSON"';
	 
	close($DATEIHANDLER);

	
}

# ---------------------------------------------------
# Control for "frmStart" Form
# This section is necessary for saving changed
# parameter to config file.
# ---------------------------------------------------
my $frmStart = $cgi->start_form(
      -name    => 'MiFloraPlugIn',
      -method => 'POST',
  );
$template->param( frmStart => $frmStart );


# ---------------------------------------------------
# Control for "frmEnd" Form
# This section is necessary for saving changed
# parameter to config file.
# ---------------------------------------------------
my $frmEnd = $cgi->end_form();
$template->param( frmEnd => $frmEnd );


# ---------------------------------------------------
# Control for "txtUSBDevice" Textfield
# ---------------------------------------------------
my $txtUSBDevice = $cgi->textfield(
      -name    => 'txtUSBDevice',
      -default => $pcfg->param('MIFLORA.USBDEVICE'),
  );
$template->param( txtUSBDevice => $txtUSBDevice );

# ---------------------------------------------------
# Control for "txtMQTTServerIP" Textfield
# ---------------------------------------------------
my $txtMQTTServerIP = $cgi->textfield(
      -name    => 'txtMQTTServerIP',
      -default => $pcfg->param('MIFLORA.MQTTSERVERIP'),
  );
$template->param( txtMQTTServerIP => $txtMQTTServerIP );

# ---------------------------------------------------
# Control for "txtMQTTServerPort" Textfield
# ---------------------------------------------------
my $txtMQTTServerPort = $cgi->textfield(
      -name    => 'txtMQTTServerPort',
      -default => $pcfg->param('MIFLORA.MQTTSERVERPORT'),
  );
$template->param( txtMQTTServerPort => $txtMQTTServerPort );

# ---------------------------------------------------
# Control for "txtMQTTServerUsername" Textfield
# ---------------------------------------------------
my $txtMQTTServerUsername = $cgi->textfield(
      -name    => 'txtMQTTServerUsername',
#	  -default => 'Enter username',
#     -default => $pcfg->param('MIFLORA.MQTTSERVERUSERNAME'),
  );
$template->param( txtMQTTServerUsername => $txtMQTTServerUsername );

# ---------------------------------------------------
# Control for "txtMQTTServerPassword" Textfield
# ---------------------------------------------------
my $txtMQTTServerPassword = $cgi->textfield(
      -name    => 'txtMQTTServerPassword',
#  	  -default => 'Enter password',
#     -default => $pcfg->param('MIFLORA.MQTTSERVERPASSWORD'),
  );
$template->param( txtMQTTServerPassword => $txtMQTTServerPassword );

# ---------------------------------------------------
# Control for "txtMQTTServerTopic" Textfield
# ---------------------------------------------------
my $txtMQTTServerTopic = $cgi->textfield(
      -name    => 'txtMQTTServerTopic',
      -default => $pcfg->param('MIFLORA.MQTTSERVERTOPIC'),
  );
$template->param( txtMQTTServerTopic => $txtMQTTServerTopic );

# ---------------------------------------------------
# Control for "btnSave" Button
# --------------------------------------------------- 
my $btnSave = $cgi->submit(
      -name    => 'btnSave',
      -value => $L{'MIFLORA.btnSave'},
  );
$template->param( btnSave => $btnSave );

# ---------------------------------------------------
# Scan for available wireless devices
# ---------------------------------------------------
my $output1 = qx(wmbusmeters --usestdoutforlogging --exitafter=30s auto:t1>$lbptemplatedir/test.dat);

#open(DATEI, "$lbptemplatedir/test.dat") or die $!;
#my @daten = <DATEI>;
#close (DATEI);

#my $daten;

open (DATEI, "<$lbptemplatedir/test.dat") or die $!;
   my $daten= LoxBerry::System::read_file("$lbptemplatedir/test.dat");
   close (DATEI);	
if (!$daten) { print "Scheisse, nicht erfolgreich" } else { print "Alles suppi!" }
$daten =~ s/\n/<br>/;
$template->param( DIEDATENAUSDEMFILE => $daten );

# Wir erzeugen eine Select-Liste mit 2 Einträgen für ON und OFF
@values = ('1', '0' );
%labels = (
      '1' => 'On',
      '0' => 'Off',
  );
my $selectlist = $cgi->popup_menu(
      -name    => 'selectlist',
      -values  => \@values,
      -labels  => \%labels,
      -default => '1',
  );
$template->param( SELECTLIST => $selectlist ); 


# Den so erzeugten HTML-Code schreiben wir ins Template.

print "Version of this plugin is " . LoxBerry::System::pluginversion() . "<br>\n";

print "Use a variable from the config file: <i>" . %pcfg{'SECTION1.NAME'} . "</i><br>\n";

$template->param( ACTIVATED => $activated);

# ---------------------------------------------------
# Localized Labels from language.ini
# ---------------------------------------------------

$template->param( lblMQTTServerIP => $L{'MIFLORA.lblMQTTServerIP'} );
$template->param( lblMQTTServerPort => $L{'MIFLORA.lblMQTTServerPort'}  );
$template->param( lblMQTTServerTopic => $L{'MIFLORA.lblMQTTServerTopic'}  );
$template->param( lblMQTTServerUsername => $L{'MIFLORA.lblMQTTServerUsername'}  );
$template->param( lblMQTTServerPassword => $L{'MIFLORA.lblMQTTServerPassword'}  );
$template->param( lbloutput => $L{'MIFLORA.lbloutput'}  );

print "Testtext\n";

# ---------------------------------------------------
# Output of all discovered wireles devices within
# selected discovering time.
# ---------------------------------------------------

#print "$daten";

# Nun wird das Template ausgegeben.
print $template->output();
  
# Schlussendlich lassen wir noch den Footer ausgeben.
LoxBerry::Web::lbfooter();
