/*
  Warnings:

  - The primary key for the `isochrones` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - Added the required column `type` to the `isochrones` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "isochrones" DROP CONSTRAINT "isochrones_pkey",
ADD COLUMN     "type" TEXT NOT NULL,
ADD CONSTRAINT "isochrones_pkey" PRIMARY KEY ("station_id", "duration", "type");
