module load Python/2.7.11-foss-2016a
curl -O https://bootstrap.pypa.io/get-pip.py
python get-pip.py --user --upgrade
rm get-pip.py
.local/bin/pip install --user --upgrade pip

git clone https://github.com/tensorflow/tensorflow
git clone https://github.com/bazelbuild/bazel.git
wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u92-b14/jdk-8u92-linux-x64.tar.gz
tar -xf jdk*
rm jdk*.gz
cd bazel
export JAVA_HOME=~/jdk1.8.0_92/
module unload GCC/4.9.3-2.25
module load GCC/4.8.2
./compile.sh
cd ../tensorflow
export PATH=/home/ulg/sysmod/gmath/bazel/output/:$PATH
./configure
bazel build -c opt //tensorflow/tools/pip_package:build_pip_package 2>/dev/null
bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
cd
.local/bin/pip install --user --upgrade /tmp/tensorflow_pkg/tensorflow-0.8.0-py2-none-any.whl