%define major 1
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

%bcond_with	jni
%bcond_with	static
%bcond_without	strict
%bcond_with	tests

Summary:	An encryption library for one-to-one and group instant messaging
Name:		lime
Version:	5.1.67
Release:	1
License:	GPLv3
Group:		System/Libraries
URL:		https://linphone.org/
Source0:	https://gitlab.linphone.org/BC/public/%{name}/-/archive/%{version}/%{name}-%{version}.tar.bz2
Patch0:		lime-5.0.18-cmake-fix-cmake-path.patch
Patch1:		lime-4.4.9-cmake-fix-pkgconfig-pc-file.patch

BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	ninja
BuildRequires:	boost-devel
BuildRequires:	soci-devel
BuildRequires:	pkgconfig(bctoolbox)

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
%{_datadir}/cmake/%{name}/

#---------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%cmake \
	-DENABLE_STRICT:BOOL=%{?with_static:ON}%{?!with_static:OFF} \
	-DENABLE_STATIC:BOOL=%{?with_static:ON}%{?!with_static:OFF} \
	-DENABLE_UNIT_TESTS:BOOL=%{?with_tests:ON}%{?!with_tests:OFF} \
	-DENABLE_JNI:BOOL=%{?with_jni:ON}%{?!with_jni:OFF} \
	-DENABLE_C_INTERFACE:BOOL=NO \
	-G Ninja

%ninja_build

%install
%ninja_install -C build

find %{buildroot} -name "*.la" -delete

