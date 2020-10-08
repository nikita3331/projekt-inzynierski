\ProvidesClass{pginz}
 
\newcommand{\headlinecolor}{\normalcolor}
\LoadClass[10pt,a4paper,twoside]{report}

\RequirePackage[a4paper,inner=3.5cm,outer=2.5cm,top=2.5cm,bottom=2.5cm]{geometry}
\linespread{1.3} %interlinia 1.5
\setlength{\parindent}{1.25cm}
\RequirePackage{indentfirst}

\RequirePackage[utf8]{inputenc}
\RequirePackage{polski}
\RequirePackage[polish]{babel}
\RequirePackage{pdfpages}

\RequirePackage[titletoc,title]{appendix}
\RequirePackage{titlesec}
\RequirePackage{uarial}
\renewcommand*{\familydefault}{\sfdefault}

%*************
\RequirePackage{newtxtext, newtxmath} %lepiej wyglądające nagłówki
\RequirePackage{epstopdf} %do dołączania obrazków w formacie eps
\RequirePackage{hyperref} % hiperłącza wewnętrzne (cytowania, odnośniki do obrazków, równań)
\RequirePackage{xcolor,listings} %listingi 
\RequirePackage[font=small,labelfont=bf]{caption} %ustawienie czcionki 9pt na podpisach
\captionsetup[table]{justification=justified,singlelinecheck=false, format=hang} %ustawienie podpisów tabel 
\RequirePackage{enumitem} %to, czego brakowało przy symbolach
%*************
\titleformat{\chapter}[hang]
{\normalfont\fontsize{12}{15}\bfseries\uppercase}{\thechapter.}{1em}{}
\titlespacing*{\chapter}{0pt}{12pt}{6pt}

\titleformat{\section}[hang]
{\normalfont\fontsize{10}{12}\bfseries\itshape}{\thesection.}{0.5em}{}
\titlespacing*{\section}{0pt}{12pt}{6pt}

\titleformat{\subsection}[hang]
{\normalfont\fontsize{10}{12}\itshape}{\thesubsection.}{0.5em}{}
\titlespacing*{\subsection}{0pt}{12pt}{6pt}
