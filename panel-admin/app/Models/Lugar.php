<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Str;

class Lugar extends Model
{
    protected $table = "lugares";

    protected $fillable  = [
            "id",
            "nombre",
            "slug",
            "descripcion",
            "categoria_id",
            "esfuerzo",
            "municipio_id","direccion","latitud","longitud","popularidad","estado"];

    protected static function booted()
    {
        static::creating(function ($lugar) {
            $lugar->slug = static::generateUniqueSlug($lugar->nombre);
        });

        static::updating(function ($lugar) {
            if ($lugar->isDirty('nombre')) {
                $lugar->slug = static::generateUniqueSlug($lugar->nombre);
            }
        });
    }

    protected static function generateUniqueSlug($nombre)
    {
        $slug = Str::slug($nombre);
        $originalSlug = $slug;
        $count = 1;

        while (static::where('slug', $slug)->exists()) {
            $slug = $originalSlug . '-' . $count++;
        }

        return $slug;
    }

    //relaciones

    public function categorias()
    {
        return $this->belongsToMany(Categoria::class);
    }

    public function municipio()
    {
        return $this->belongsTo(Municipio::class);
    }

    public function imagenes()
    {
        return $this->hasMany(LugarImagen::class);
    }

    public function imagenPrincipal()
    {
        return $this->hasOne(LugarImagen::class)
            ->where('is_principal', true);
    }

    protected $casts = [
        'estado' => 'boolean'
    ];

}
