<?php

namespace App\Filament\Resources\Lugars;

use App\Filament\Resources\Lugars\Pages\CreateLugar;
use App\Filament\Resources\Lugars\Pages\EditLugar;
use App\Filament\Resources\Lugars\Pages\ListLugars;
use App\Filament\Resources\Lugars\Schemas\LugarForm;
use App\Filament\Resources\Lugars\Tables\LugarsTable;
use App\Models\Lugar;
use BackedEnum;
use Filament\Resources\Resource;
use Filament\Schemas\Schema;
use Filament\Support\Icons\Heroicon;
use Filament\Tables\Table;

class LugarResource extends Resource
{
    protected static ?string $model = Lugar::class;

    protected static string|BackedEnum|null $navigationIcon = Heroicon::OutlinedMap;
    protected static ?string $navigationLabel = 'Sitios turísticos';

    public static function form(Schema $schema): Schema
    {
        return LugarForm::configure($schema);
    }

    public static function table(Table $table): Table
    {
        return LugarsTable::configure($table);
    }

    public static function getRelations(): array
    {
        return [
            //
        ];
    }

    public static function getPages(): array
    {
        return [
            'index' => ListLugars::route('/'),
            'create' => CreateLugar::route('/create'),
            'edit' => EditLugar::route('/{record}/edit'),
        ];
    }
}
