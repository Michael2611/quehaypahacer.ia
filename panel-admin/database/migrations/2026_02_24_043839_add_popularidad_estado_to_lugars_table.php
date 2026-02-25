<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::table('lugares', function (Blueprint $table) {
            $table->integer('popularidad')->default(0); // Puedes ajustar el tipo y valor por defecto
            $table->boolean('estado')->default(true);  // true = activo, false = inactivo
        });
    }

    public function down(): void
    {
        Schema::table('lugares', function (Blueprint $table) {
            $table->dropColumn(['popularidad', 'estado']);
        });
    }
};
