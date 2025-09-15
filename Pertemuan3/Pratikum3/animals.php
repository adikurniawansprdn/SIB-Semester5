<?php

class Animal {
    public $animals;

    public function __construct() {
        $this->animals = ['Ayam', 'Ikan'];
    }
    public function index() {
        foreach ($this->animals as $animal) {
            echo $animal , '<br>';
        }
    }
    public function store($animal) {
        array_push($this->animals, $animal);
    }
    public function update($index, $newanimal) { 
            $animal = $this->animals[$index];
            $this->animals[$index] = $newanimal;  
    }
    public function destroy($index) {
       array_splice($this->animals, $index,1);
    }
}

$animal = new Animal();

echo 'Index Menampilkan seluruh hewan:<br>';
$animal->index();
echo '<br>';

echo 'Store Menambahkan hewan baru (burung):<br>';
$animal->store('Burung');
$animal->index();
echo '<br>';

echo 'Update Mengupdate hewan:<br>';
$animal->update(0, 'Kucing Anggora');
$animal->index();
echo '<br>';

echo 'Destroy Menghapus hewan:<br>';
$animal->destroy(1);
$animal->index();
echo '<br>';

?>