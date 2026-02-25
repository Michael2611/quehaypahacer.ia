<?php

namespace App\Filament\Resources\Lugars\Tables;

use Filament\Actions\BulkActionGroup;
use Filament\Actions\DeleteBulkAction;
use Filament\Tables\Table;
use Filament\Tables\Columns\TextColumn;
use Filament\Actions\ActionGroup;
use Filament\Actions\DeleteAction;
use Filament\Actions\EditAction;
use Filament\Actions\ViewAction;
use Filament\Actions\Action;
use Maatwebsite\Excel\Facades\Excel;
use App\Imports\LugaresImport;
use Filament\Forms\Components\FileUpload;

class LugarsTable
{
    public static function configure(Table $table): Table
    {
        return $table
            ->columns([
                TextColumn::make('id'),
                TextColumn::make('nombre')
                    ->searchable(),
                TextColumn::make('municipio.nombre'),
                TextColumn::make('categorias.nombre')
                    ->label('Categorías')
                    ->badge()
                    ->separator(',')
                    ->sortable()
                    ->searchable(),
            ])
            ->headerActions([
                Action::make('Importar CSV')
                    ->form([
                        FileUpload::make('archivo')
                            ->label('Archivo CSV')
                            ->required()
                            ->acceptedFileTypes(['text/csv', 'text/plain', '.csv'])
                            ->disk('local'),
                    ])
                    ->action(function ($data) {
                        Excel::import(new LugaresImport, $data['archivo']);
                        \Filament\Notifications\Notification::make()
                            ->title('¡Importación completada!')
                            ->success()
                            ->send();
                    })
                    ->button()
            ])
            ->filters([
                //
            ])
            ->recordActions([
                ActionGroup::make([
                    ViewAction::make(),
                    EditAction::make(),
                    DeleteAction::make(),
                ]),
            ])
            ->toolbarActions([
                BulkActionGroup::make([
                    DeleteBulkAction::make(),
                ]),
            ]);
    }
}
