# 環境設定メモ

以下は，筆者個人の計算機設定に関わるメモである．本リポジトリのスクリプトを実行するために **必要というわけではない**．

## curl

```
wget https://curl.se/download/curl-7.76.1.tar.gz
tar xf curl-7.76.1.tar.gz 
cd curl-7.76.1/
./configure --prefix=$HOME/.local
nice make -j10
make install
```

## git

```
git clone https://github.com/git/git.git
cd git/
make configure
./configure --prefix=$HOME/.local
nice make -j10
make install
```

## git-lfs

```
wget https://github.com/git-lfs/git-lfs/releases/download/v2.13.3/git-lfs-linux-amd64-v2.13.3.tar.gz
mkdir git-lfs
tar xf ../git-lfs-linux-amd64-v2.13.3.tar.gz
cp -p git-lfs ${HOME}/.local/bin/
```
