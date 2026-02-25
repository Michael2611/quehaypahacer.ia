<?php

namespace App\Filament\Widgets;

use App\Models\Departamento;
use App\Models\Municipio;
use App\Models\Categoria;
use App\Models\Lugar;
use Filament\Widgets\StatsOverviewWidget;
use Filament\Widgets\StatsOverviewWidget\Stat;

class EstadisticasGenerales extends StatsOverviewWidget
{
    protected function getStats(): array
    {
        return [
            Stat::make('Departamentos', Departamento::count())
                ->description('Total registrados')
                ->icon('heroicon-o-building-office'),

            Stat::make('Municipios', Municipio::count())
                ->description('Total registrados')
                ->icon('heroicon-o-map'),

            Stat::make('Categorías', Categoria::count())
                ->description('Total registradas')
                ->icon('heroicon-o-tag'),

            Stat::make('Lugares', Lugar::count())
                ->description('Total registrados')
                ->icon('heroicon-o-map-pin'),
        ];
    }
}
