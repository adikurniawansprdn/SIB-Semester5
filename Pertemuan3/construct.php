<?php
class person {
    public $nama;
    public $jurusan;
    public $alamat;

    public function __construct($nama,$jurusan,$alamat){
        $this ->nama = $nama;
        $this ->jurusan = $jurusan;
        $this ->alamat = $alamat;
    }
    public function cetak(){
        echo 'Nama',$this->nama;
        echo 'Jurusan',$this->jurusan;
        echo 'Alamat',$this->alamat;
    }
}  
?>