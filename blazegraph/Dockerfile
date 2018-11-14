FROM centos:centos7

# Sets working directory to /data
WORKDIR /data

# Install Java
RUN yum install -y java && yum clean all

# Download Blazegraph
RUN curl -L http://downloads.sourceforge.net/project/bigdata/bigdata/2.1.1/blazegraph.jar > blazegraph.jar

# Starts Blazegraph server
CMD ["java", "-Djetty.start.timeout=45", "-jar", "blazegraph.jar"]