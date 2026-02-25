<?php

namespace App\Filament\Resources\Municipios\Schemas;

use Filament\Forms\Components\TextInput;
use Filament\Schemas\Schema;
use Filament\Forms\Components\Select;

class MunicipioForm
{
    public static function configure(Schema $schema): Schema
    {
        return $schema
            ->components([
                TextInput::make('nombre')
                    ->required(),
                Select::make('departamento_id')
                ->relationship('departamento', 'nombre')
                ->required(),
            ]);
    }
}
