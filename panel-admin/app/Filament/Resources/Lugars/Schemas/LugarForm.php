<?php

namespace App\Filament\Resources\Lugars\Schemas;

use Filament\Schemas\Schema;
use Filament\Forms;
use Filament\Tables;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Forms\Components\Textarea;
use Filament\Forms\Components\Toggle;
use Filament\Forms\Components\FileUpload;
use Filament\Forms\Components\Repeater;
use Illuminate\Support\Str;

class LugarForm
{
    public static function configure(Schema $schema): Schema
    {
        return $schema
            ->components([
                TextInput::make('nombre')
                    ->required()
                    ->maxLength(255)
                    ->live(onBlur: true)
                    ->afterStateUpdated(fn ($state, callable $set) =>
                        $set('slug', Str::slug($state))
                    ),

                TextInput::make('slug')
                    ->required()
                    ->unique(ignoreRecord: true),

                Textarea::make('descripcion'),

                Select::make('categorias')
                    ->relationship('categorias', 'nombre')
                    ->multiple()
                    ->preload()
                    ->searchable()
                    ->required(),

                Select::make('esfuerzo')
                    ->label('Esfuerzo')
                    ->options([
                        'alto' => 'Alto',
                        'medio' => 'Medio',
                        'bajo' => 'Bajo',
                    ])
                    ->searchable()
                    ->required(),

                Select::make('municipio_id')
                    ->relationship('municipio', 'nombre')
                    ->required(),

                TextInput::make('direccion'),

                TextInput::make('popularidad')
                ->numeric()
                ->default(0),

                TextInput::make('latitud')
                    ->numeric(),

                TextInput::make('longitud')
                    ->numeric(),

                Toggle::make('estado')
                    ->label('Activo')
                    ->default(true),

                Repeater::make('imagenes')
                    ->relationship()
                    ->schema([
                        FileUpload::make('url')
                            ->image()
                            ->disk('public')
                            ->directory('lugares')
                            ->required(),

                        Toggle::make('is_principal')
                            ->label('Imagen principal'),
                    ]),
            ]);
    }
}
