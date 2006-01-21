Summary:	A language for scientific illustration
Summary(pl):	Jêzyk s³u¿±cy do tworzenia ilustracji i wykresów naukowych
Name:		gri
Version:	2.12.9
Release:	1
License:	GPL
Group:		Applications/Engineering
Source0:	http://dl.sourceforge.net/gri/%{name}-%{version}.tgz
# Source0-md5:	f4e0841ae78b439c7262d109bc2932d6
Patch0:		%{name}-etc_dir.patch
URL:		http://gri.sourceforge.net/
BuildRequires:	ImageMagick
BuildRequires:	ghostscript
BuildRequires:	ghostscript-fonts-std
BuildRequires:	libstdc++-devel
BuildRequires:	perl-modules
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _noautocompressdoc      *.ps *.html *.gri *.dat

%description
Gri is a language for scientific graphics programming. It is a
command-driven application, as opposed to a click/point application.
It is analogous to latex, and shares the property that extensive power
is the reward for tolerating a modest learning curve. Gri output is in
industry-standard PostScript, suitable for incorporation in documents
prepared by various text processors.

Gri can make x-y graphs, contour-graphs, and image graphs. In addition
to high-level capabilities, it has enough low-level capabilities to
allow users to achieve a high degree of customization. Precise control
is extended to all aspects of drawing, including line-widths, colors,
and fonts. Text includes a subset of the tex language, so that it is
easy to incorporate Greek letters and mathematical symbols in labels.

The following is a terse yet working Gri program. If it is stored in a
file called 'example.gri', and executed with the unix command 'gri
example', it will create a postscript file called 'example.ps' with a
linegraph connecting data points in the file called `file.dat'.

  open file.dat		# open a file with columnar data
  read columns x * y	# read first column as x and third as y
  draw curve		# draw line through data (autoscaled axes)


%description -l pl
Gri jest jêzykiem programowania stworzonym do tworzenia naukowych
ilustracji i wykresów. Jest sterowany poleceniami, a nie klikaniem.
Czêsto jest porównywany do LaTeXa w kontek¶cie du¿ych mo¿liwo¶ci
wp³ywania na koñcowy rezultat. Gri generuje na wyj¶ciu standardowy
PostScript, który mo¿na do³±czaæ do dokumentów przygotowywanych przez
ró¿ne procesory tekstu.

Gri potrafi wygenerowaæ szereg ró¿nych typów wykresów: dwuwymiarowe,
konturowe i graficzne. Oprócz mo¿liwo¶ci wysokopoziomowych ma tak¿e
wystarczaj±ce mo¿liwo¶ci niskopoziomowe, aby pozwoliæ u¿ytkownikom na
du¿y stopieñ dostosowania. Mo¿liwa jest precyzyjna kontrola wszystkich
aspektów rysowania, w³±czenie z grubo¶ciami linii, kolorami i fontami.
Obs³uga tekstu to podzbiór jêzyka TeX, co pozwala na ³atwe
wykorzystanie greckich liter i symboli matematycznych w etykietach.

Poni¿ej znajduje siê przyk³ad krótkiego dzia³aj±cego programu w Gri.
Je¶li bêdzie zapisany w pliku 'example.gri' i potraktowany poleceniem
'gri example', utworzy plik postscriptowy 'example.ps' z wykresem
liniowym ³±cz±cym punkty pobrane z pliku 'file.dat'.

  open file.dat		# otworzenie pliku z kolumnami danych
  read columns x * y	# odczytanie 1. kolumny jako x i 3. jako y
  draw curve		# narysowanie linii przez dane (autoskalowanej)

%prep
%setup -q
%patch0 -p1

%build
%configure2_13

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	DOC_DIR=../docinst

# fixing stupid 'make install' results
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install doc/gri-manpage.1 $RPM_BUILD_ROOT%{_mandir}/man1/gri.1
install doc/gri_*.1 $RPM_BUILD_ROOT%{_mandir}/man1

mv -f $RPM_BUILD_ROOT{%{_prefix}/info,%{_infodir}}
rm -f $RPM_BUILD_ROOT%{_bindir}/%{name}
mv -f $RPM_BUILD_ROOT%{_bindir}/{%{name}-%{version},%{name}}

cd $RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}

cat startup.msg | sed -e "s,$RPM_BUILD_ROOT,%{_prefix}," >tmp
mv tmp startup.msg

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc AUTHOR README copyright.txt
%doc docinst/html docinst/examples
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man?/*
%{_infodir}/*.info*
%{_datadir}/%{name}
