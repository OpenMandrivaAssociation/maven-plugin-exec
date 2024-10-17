Name:           maven-plugin-exec
Version:        1.1
Release:        4
Summary:        Exec Maven Plugin

Group:          Development/Java
License:        ASL 2.0
URL:            https://mojo.codehaus.org/exec-maven-plugin
# The source tarball has been generated from upstream VCS:
# svn export https://svn.codehaus.org/mojo/tags/exec-maven-plugin-%{version} 
#            %{name}-%{version}
# tar cjvf %{name}-%{version}.tar.bz2 %{name}-%{version}
Source0:        %{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: maven2
BuildRequires: maven2-common-poms >= 1.0-10
BuildRequires: plexus-utils
BuildRequires: plexus-container-default
BuildRequires: maven-shared-plugin-testing-harness
BuildRequires: maven2-plugin-remote-resources
BuildRequires: maven2-plugin-plugin
BuildRequires: maven2-plugin-resources
BuildRequires: maven2-plugin-compiler
BuildRequires: maven2-plugin-install
BuildRequires: maven2-plugin-jar
BuildRequires: maven2-plugin-javadoc
BuildRequires: maven2-plugin-enforcer
BuildRequires: maven-surefire-maven-plugin
BuildRequires: maven-doxia-sitetools
Requires: maven2
Requires: plexus-utils
Requires: plexus-container-default
Requires: maven-shared-plugin-testing-harness
Requires(post): jpackage-utils
Requires(postun): jpackage-utils

%description
A plugin to allow execution of system and Java programs

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.


%prep
%setup -q 

#there is nothing under MIT license
rm -f LICENSE.txt

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven.test.skip=true \
        install javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}/%{name}
install -m 644 target/exec-maven-plugin-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar

(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; \
    do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%add_to_maven_depmap org.codehaus.mojo exec-maven-plugin %{version} JPP maven-plugin-exec

# poms
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
install -pm 644 pom.xml \
    %{buildroot}%{_datadir}/maven2/poms/JPP-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
rm -rf target/site/api*

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{_datadir}/maven2/poms/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

