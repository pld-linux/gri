
Summary: A language for scientific illustration
Summary(pl): Jêzyk s³u¿±cy do tworzenia ilustracji, wykresów naukowych
Name: gri
Version: 2.12.1
Release: 1
License: GPL
Group: Applications/Engineering
Source: http://ftp1.sourceforge.net/gri/%{name}-%{version}.tgz
URL: http://gri.sourceforge.net
Icon: grilogo.gif

BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _noautocompressdoc      *.ps *.html *.gri *.dat

%description
Gri is a language for scientific graphics programming.  It is a
command-driven application, as opposed to a click/point application.
It is analogous to latex, and shares the property that extensive power
is the reward for tolerating a modest learning curve.  Gri output is
in industry-standard PostScript, suitable for incorporation in
documents prepared by various text processors.

Gri can make x-y graphs, contour-graphs, and image graphs.  In
addition to high-level capabilities, it has enough low-level
capabilities to allow users to achieve a high degree of customization.
Precise control is extended to all aspects of drawing, including
line-widths, colors, and fonts.  Text includes a subset of the tex
language, so that it is easy to incorporate Greek letters and
mathematical symbols in labels.

The following is a terse yet working Gri program.  If it is stored in
a file called 'example.gri', and executed with the unix command 'gri
example', it will create a postscript file called 'example.ps' with
a linegraph connecting data points in the file called `file.dat'.

   open file.dat        # open a file with columnar data
   read columns x * y   # read first column as x and third as y
   draw curve           # draw line through data (autoscaled axes)


%description -l pl
Gri jest jêzykiem programowania stworzonym do tworzenia naukowych
ilustracji, wykresów. Czêsto jest porównywany do latexa w kontek¶cie
du¿ych mo¿liwo¶ci wp³ywania na koñcowy rezultat.

Gri potrafi wygenerowaæ szereg ró¿nych typów wykresów. Formatem
plików wynikowych jest PostScript.

%prep
%setup -q

%build
%configure2_13 
%{__make} gri

%install
rm -rf $RPM_BUILD_ROOT


%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	DOC_DIR=../docinst 

# fixing stupid 'make install' results
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install doc/gri-manpage.1 $RPM_BUILD_ROOT%{_mandir}/man1/gri.1
install doc/gri_*.1 $RPM_BUILD_ROOT%{_mandir}/man1

cd $RPM_BUILD_ROOT
mv .%{_prefix}/info/ .%{_infodir}

rm .%{_bindir}/%{name}
mv .%{_bindir}/%{name}-%{version} .%{_bindir}/%name

cd $RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}

cat startup.msg | sed -e "s,$RPM_BUILD_ROOT,%{_prefix}," >tmp
mv tmp startup.msg
	        


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHOR README copyright.txt
%doc docinst/html docinst/examples
%attr(755,root,root) %{_bindir}/*
%{_mandir}/*/*
%{_infodir}/*

%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/%{version}
%{_datadir}/%{name}/%{version}/*


%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
