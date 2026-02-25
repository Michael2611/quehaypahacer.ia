<?php

namespace App\Filament\Resources\Lugars\Pages;

use App\Filament\Resources\Lugars\LugarResource;
use Filament\Actions\CreateAction;
use Filament\Resources\Pages\ListRecords;

class ListLugars extends ListRecords
{
    protected static string $resource = LugarResource::class;

    protected function getHeaderActions(): array
    {
        return [
            CreateAction::make(),
        ];
    }
}
