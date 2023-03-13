#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	5.104
%define		qtver		5.15.2
%define		kfname		kbookmarks

Summary:	Web browser bookmark management
Name:		kf5-%{kfname}
Version:	5.104.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	7cf5a623184fd2c1f41b5d46a5a442cf
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	Qt5Xml-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	kf5-kcodecs-devel >= %{version}
BuildRequires:	kf5-kconfig-devel >= %{version}
BuildRequires:	kf5-kconfigwidgets-devel >= %{version}
BuildRequires:	kf5-kcoreaddons-devel >= %{version}
BuildRequires:	kf5-kwidgetsaddons-devel >= %{version}
BuildRequires:	kf5-kxmlgui-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt5DBus >= %{qtver}
Requires:	Qt5Widgets >= %{qtver}
Requires:	Qt5Xml >= %{qtver}
Requires:	kf5-kcodecs >= %{version}
Requires:	kf5-kconfig >= %{version}
Requires:	kf5-kconfigwidgets >= %{version}
Requires:	kf5-kcoreaddons >= %{version}
Requires:	kf5-kwidgetsaddons >= %{version}
Requires:	kf5-kxmlgui >= %{version}
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
KBookmarks lets you access and manipulate bookmarks stored using the
XBEL format: http://pyxml.sourceforge.net/topics/xbel/

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Widgets-devel >= %{qtver}
Requires:	Qt5Xml-devel >= %{qtver}
Requires:	cmake >= 3.16
Requires:	kf5-kwidgetsaddons-devel >= %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%ninja_build

%if %{with tests}
ctest
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF5Bookmarks.so.5
%attr(755,root,root) %{_libdir}/libKF5Bookmarks.so.*.*
%{_datadir}/qlogging-categories5/kbookmarks.categories
%{_datadir}/qlogging-categories5/kbookmarks.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KBookmarks
%{_libdir}/cmake/KF5Bookmarks
%{_libdir}/libKF5Bookmarks.so
%{qt5dir}/mkspecs/modules/qt_KBookmarks.pri
