<?php

namespace App\Controllers;
use App\Models\PengawasanModel;

class Home extends BaseController
{
    public function index()
    {
        $model = new PengawasanModel();
        // Mengambil seluruh data hasil ETL Airflow
        $data['pengawasan'] = $model->findAll();

        return view('dashboard_v1', $data);
    }
}