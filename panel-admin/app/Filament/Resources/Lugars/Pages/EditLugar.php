<?php

namespace App\Filament\Resources\Lugars\Pages;

use App\Filament\Resources\Lugars\LugarResource;
use Filament\Actions\DeleteAction;
use Filament\Resources\Pages\EditRecord;

class EditLugar extends EditRecord
{
    protected static string $resource = LugarResource::class;

    protected function getHeaderActions(): array
    {
        return [
            DeleteAction::make(),
        ];
    }
}
