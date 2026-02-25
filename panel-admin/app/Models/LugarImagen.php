<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class LugarImagen extends Model
{
    protected $fillable = [
        "lugar_id",
        "url",
    ];


    protected static function booted()
    {
        static::creating(function ($imagen) {

            $existePrincipal = self::where('lugar_id', $imagen->lugar_id)
                ->where('is_principal', true)
                ->exists();

            if (! $existePrincipal) {
                $imagen->is_principal = true;
            }
        });
    }

    public function imagenes()
    {
        return $this->hasMany(LugarImagen::class);
    }

}
