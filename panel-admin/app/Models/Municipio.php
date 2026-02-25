<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Municipio extends Model
{

    protected $fillable= ["id","nombre","departamento_id"];

    public function departamento()
    {
        return $this->belongsTo(Departamento::class);
    }

    public function lugares()
    {
        return $this->hasMany(Lugar::class);
    }
}
