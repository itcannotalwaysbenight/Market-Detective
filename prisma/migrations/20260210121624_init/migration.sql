-- CreateTable
CREATE TABLE "PropertyPro" (
    "id" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "url" TEXT NOT NULL,
    "description" TEXT,
    "address" TEXT NOT NULL,
    "addressNumber" TEXT,
    "city" TEXT NOT NULL,
    "state" TEXT,
    "country" TEXT NOT NULL DEFAULT 'Nigeria',
    "latitude" DOUBLE PRECISION,
    "longitude" DOUBLE PRECISION,
    "images" TEXT[] DEFAULT ARRAY[]::TEXT[],
    "videos" TEXT[] DEFAULT ARRAY[]::TEXT[],
    "threeDModel" TEXT,
    "priceMonthly" INTEGER NOT NULL,
    "beds" INTEGER NOT NULL,
    "baths" INTEGER NOT NULL,
    "sqft" INTEGER,
    "yearBuilt" INTEGER,
    "amenities" TEXT[] DEFAULT ARRAY[]::TEXT[],
    "petFriendly" BOOLEAN NOT NULL DEFAULT false,
    "furnished" BOOLEAN NOT NULL DEFAULT false,
    "airConditioned" BOOLEAN NOT NULL DEFAULT false,
    "minLeaseTerm" INTEGER NOT NULL DEFAULT 12,
    "availabilityDate" TIMESTAMP(3),
    "leaseLengthMonths" INTEGER,
    "utilitiesIncluded" TEXT[] DEFAULT ARRAY[]::TEXT[],
    "smokingAllowed" BOOLEAN NOT NULL DEFAULT false,
    "visitorPolicy" TEXT,
    "views" INTEGER NOT NULL DEFAULT 0,
    "favoriteCount" INTEGER NOT NULL DEFAULT 0,
    "matchCount" INTEGER NOT NULL DEFAULT 0,
    "publishedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "PropertyPro_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Jiji" (
    "id" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "url" TEXT NOT NULL,
    "description" TEXT,
    "address" TEXT NOT NULL,
    "addressNumber" TEXT,
    "city" TEXT NOT NULL,
    "state" TEXT,
    "country" TEXT NOT NULL DEFAULT 'Nigeria',
    "latitude" DOUBLE PRECISION,
    "longitude" DOUBLE PRECISION,
    "images" TEXT[] DEFAULT ARRAY[]::TEXT[],
    "videos" TEXT[] DEFAULT ARRAY[]::TEXT[],
    "threeDModel" TEXT,
    "priceMonthly" INTEGER NOT NULL,
    "beds" INTEGER NOT NULL,
    "baths" INTEGER NOT NULL,
    "sqft" INTEGER,
    "yearBuilt" INTEGER,
    "amenities" TEXT[] DEFAULT ARRAY[]::TEXT[],
    "petFriendly" BOOLEAN NOT NULL DEFAULT false,
    "furnished" BOOLEAN NOT NULL DEFAULT false,
    "airConditioned" BOOLEAN NOT NULL DEFAULT false,
    "minLeaseTerm" INTEGER NOT NULL DEFAULT 12,
    "availabilityDate" TIMESTAMP(3),
    "leaseLengthMonths" INTEGER,
    "utilitiesIncluded" TEXT[] DEFAULT ARRAY[]::TEXT[],
    "smokingAllowed" BOOLEAN NOT NULL DEFAULT false,
    "visitorPolicy" TEXT,
    "views" INTEGER NOT NULL DEFAULT 0,
    "favoriteCount" INTEGER NOT NULL DEFAULT 0,
    "matchCount" INTEGER NOT NULL DEFAULT 0,
    "publishedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Jiji_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "PropertyPro_url_key" ON "PropertyPro"("url");

-- CreateIndex
CREATE INDEX "PropertyPro_city_idx" ON "PropertyPro"("city");

-- CreateIndex
CREATE INDEX "PropertyPro_priceMonthly_idx" ON "PropertyPro"("priceMonthly");

-- CreateIndex
CREATE INDEX "PropertyPro_beds_idx" ON "PropertyPro"("beds");

-- CreateIndex
CREATE INDEX "PropertyPro_latitude_longitude_idx" ON "PropertyPro"("latitude", "longitude");

-- CreateIndex
CREATE INDEX "PropertyPro_publishedAt_idx" ON "PropertyPro"("publishedAt");

-- CreateIndex
CREATE UNIQUE INDEX "Jiji_url_key" ON "Jiji"("url");

-- CreateIndex
CREATE INDEX "Jiji_city_idx" ON "Jiji"("city");

-- CreateIndex
CREATE INDEX "Jiji_priceMonthly_idx" ON "Jiji"("priceMonthly");

-- CreateIndex
CREATE INDEX "Jiji_beds_idx" ON "Jiji"("beds");

-- CreateIndex
CREATE INDEX "Jiji_latitude_longitude_idx" ON "Jiji"("latitude", "longitude");

-- CreateIndex
CREATE INDEX "Jiji_publishedAt_idx" ON "Jiji"("publishedAt");
