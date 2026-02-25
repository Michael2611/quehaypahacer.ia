<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Categoria extends Model
{
    protected $fillable  = ["id","nombre","descripcion","created_at","updated_at"];

    public function lugares()
    {
        return $this->belongsToMany(Lugar::class);
    }
}
