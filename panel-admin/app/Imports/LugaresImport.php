<?php

namespace App\Imports;

use App\Models\Lugar;
use App\Models\Municipio;
use App\Models\Categoria;
use App\Models\Departamento;
use Maatwebsite\Excel\Concerns\ToModel;
use Maatwebsite\Excel\Concerns\WithHeadingRow;

class LugaresImport implements ToModel, WithHeadingRow
{
    /**
    * @param array $row
    *
    * @return \Illuminate\Database\Eloquent\Model|null
    */
    public function model(array $row)
    {
        $row = array_change_key_case($row, CASE_LOWER); // para evitar mayúsculas/minúsculas

        $municipioNombre = trim($row['municipio']);
        $municipio = Municipio::whereRaw('LOWER(nombre) = ?', [mb_strtolower($municipioNombre)])->first();

        // Crear lugar
        $lugar = Lugar::create([
            'nombre' => $row['nombre'] ?? 'Sin nombre',
            'descripcion' => $row['descripcion'] ?? null,
            'municipio_id' => $municipio->id,
            'direccion' => $row['direccion'] ?? null,
            'latitud' => $row['latitud'] ?? null,
            'longitud' => $row['longitud'] ?? null,
        ]);

        // Categorías múltiples
        if (!empty($row['categorias'])) {
            $categorias = explode(',', $row['categorias']);
            $categoriaIds = [];
            foreach ($categorias as $catNombre) {
                $categoria = Categoria::firstOrCreate([
                    'nombre' => trim($catNombre)
                ]);
                $categoriaIds[] = $categoria->id;
            }
            $lugar->categorias()->sync($categoriaIds);
        }

        return $lugar;
    }
}
