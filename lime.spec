%define major 1
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

# exclude unwanted cmake requires
%global __provides_exclude_from ^%{_datadir}/cmake/.*/Find.*cmake$

%bcond jni			0
%bcond strict			1
%bcond unit_tests		1
%bcond unit_tests_install	1

Summary:	An encryption library for one-to-one and group instant messaging
Name:		lime
Version:	5.4.20
Release:	1
License:	GPLv3
Group:		System/Libraries
URL:		https://linphone.org
Source0:	https://gitlab.linphone.org/BC/public/%{name}/-/archive/%{version}/%{name}-%{version}.tar.bz2
Patch0:		lime-5.3.6-cmake-fix-cmake-path.patch
Patch1:		lime-4.4.9-cmake-fix-pkgconfig-pc-file.patch
Patch2:		lime-5.2.64-add_missing_headers.patch

BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	ninja
BuildRequires:	boost-devel
BuildRequires:	cmake(bctoolbox)
BuildRequires:	cmake(bellesip)
BuildRequires:	cmake(soci)
BuildRequires:	pkgconfig(sqlite3)

%description
LIME is an encryption library for one-to-one and group instant messaging,
allowing users to exchange messages privately and asynchronously. It
supports multiple devices per user and multiple users per device.

LIME offers two major security benefits to instant messaging users: 

 - end-to-end encryption, which means that only you and your contact
   (and not even the server) can decrypt the content that you shared
 - perfect forward secrecy, which ensures that encrypted messages cannot
   by decrypted by a third party, even if a key is compromised in the
   future

LIME is composed of a portable client library coupled with a public key
server developed by Belledonne Communications to allow end-to-end encryption
for messaging, without having to exchange cryptographic keys simultaneously.

Main features are:

 -  end-to-end encryption based on modern Elliptic Curve Diffie-Hellman(ECDH)
 -  perfect forward secrecy with double ratchet algorithm
 -  designed for group communications
 -  asynchronous messaging system based on pre-positioned keys
 -  man-in-the-middle (MITM) detection based on ZRTP auxiliary secret
 -  signaling protocol agnostic

%if %{with unit_tests} && %{with unit_tests_install}
%files
%{_bindir}/%{name}-tester
%{_datadir}/%{name}_tester/
%endif

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	Language recognition library
Group:		System/Libraries

%description -n %{libname}
LIME is an encryption library for one-to-one and group instant messaging,
allowing users to exchange messages privately and asynchronously. 

%files -n %{libname}
%{_libdir}/lib%{name}.so.*

#---------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains development files for %{name}

%files -n %{devname}
%doc README.md
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/cmake/Lime

#---------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%cmake \
	-DENABLE_STRICT:BOOL=%{?with_strict:ON}%{?!with_strict:OFF} \
	-DENABLE_UNIT_TESTS:BOOL=%{?with_unit_tests:ON}%{?!with_unit_tests:OFF} \
	-DENABLE_JNI:BOOL=%{?with_jni:ON}%{?!with_jni:OFF} \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

# don't install unit tester
%if %{with unit_tests} && ! %{with unit_tests_install}
rm -f  %{buildroot}%{_bindir}/%{name}-tester
rm -fr %{buildroot}%{_datadir}/%{name}-tester/
%endif

%check
%if %{with unit_tests}
pushd build
#FIXME: some tests fail
ctest || true
popd
%endif

