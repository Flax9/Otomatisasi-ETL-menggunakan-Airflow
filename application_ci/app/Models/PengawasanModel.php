<?php

namespace App\Models;
use CodeIgniter\Model;

class PengawasanModel extends Model
{
    protected $table      = 'stg_pengawasan_dashboard'; 
    protected $primaryKey = 'id_pengawasan'; // Sesuaikan dengan screenshot Anda
    protected $returnType = 'array';
}