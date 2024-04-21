// Fill out your copyright notice in the Description page of Project Settings.


#include "PlaneTrack.h"

// Sets default values
APlaneTrack::APlaneTrack()
{
  // Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
  PrimaryActorTick.bCanEverTick = true;

  // Initialize the track
  SplineTrack = CreateDefaultSubobject<USplineComponent>(TEXT("SplineTrack"));
  // This lets us visualize the spline in Play mode
  SplineTrack->SetDrawDebug(true);                                            
  // Set the color of the spline
  SplineTrack->SetUnselectedSplineSegmentColor(FLinearColor(1.f, 0.f, 0.f));                              
}

// Called when the game starts or when spawned
void APlaneTrack::BeginPlay()
{
	Super::BeginPlay();
	
}

// Called every frame
void APlaneTrack::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

}


void APlaneTrack::LoadSplineTrackPoints()
{
    if (this->AircraftsRawDataTable != nullptr && this->CesiumGeoreference != nullptr)
    {
        int32 PointIndex = 0;
        for (auto& row : this->AircraftsRawDataTable->GetRowMap())
        {
            FAircraftRawData* Point = (FAircraftRawData*)row.Value;

            // Get row data point in lat/long/alt and prepare it for transformation
            FVector LongitudeLatitudeHeight(Point->Longitude, Point->Latitude, Point->Height);

            // Transform the geographic coordinates to Unreal Engine coordinates
            FVector SplinePointPosition = this->CesiumGeoreference->TransformLongitudeLatitudeHeightPositionToUnreal(LongitudeLatitudeHeight);
            this->SplineTrack->AddSplinePointAtIndex(SplinePointPosition, PointIndex, ESplineCoordinateSpace::World, false);

            // Unfortunately, without direct access to a method like GetGeoTransforms (which is deprecated),
            // determining the up vector for orientation directly from CesiumGeoreference requires a custom approach.
            // For now, let's focus on fixing the coordinate transformation issue.

            PointIndex++;
        }
        this->SplineTrack->UpdateSpline();
    }
}



/*void APlaneTrack::LoadSplineTrackPoints()
{
    if (this->AircraftsRawDataTable != nullptr && this->CesiumGeoreference != nullptr)
    {
        int32 PointIndex = 0;
        for (auto& row : this->AircraftsRawDataTable->GetRowMap())
        {
            FAircraftRawData* Point = (FAircraftRawData*)row.Value;
            // Get row data point in lat/long/alt and transform it into UE4 points
            double PointLatitude = Point->Latitude;
            double PointLongitude = Point->Longitude;
            double PointHeight = Point->Height;

            // Compute the position in UE coordinates
            glm::dvec3 UECoords = this->CesiumGeoreference->TransformLongitudeLatitudeHeightToUnreal(glm::dvec3(PointLongitude, PointLatitude, PointHeight));
            FVector SplinePointPosition = FVector(UECoords.x, UECoords.y, UECoords.z);
            this->SplineTrack->AddSplinePointAtIndex(SplinePointPosition, PointIndex, ESplineCoordinateSpace::World, false);

            // Get the up vector at the position to orient the aircraft
            const CesiumGeospatial::Ellipsoid& Ellipsoid = CesiumGeospatial::Ellipsoid::WGS84;
            glm::dvec3 upVector = Ellipsoid.geodeticSurfaceNormal(CesiumGeospatial::Cartographic(FMath::DegreesToRadians(PointLongitude), FMath::DegreesToRadians(PointLatitude), FMath::DegreesToRadians(PointHeight)));

            // Compute the up vector at each point to correctly orient the plane
            glm::dvec4 ecefUp(upVector, 0.0);
            const GeoTransforms& geoTransforms = this->CesiumGeoreference->GetGeoTransforms();
            const glm::dmat4& ecefToUnreal = geoTransforms.GetEllipsoidCenteredToAbsoluteUnrealWorldTransform();
            glm::dvec4 unrealUp = ecefToUnreal * ecefUp;
            this->SplineTrack->SetUpVectorAtSplinePoint(PointIndex, FVector(unrealUp.x, unrealUp.y, unrealUp.z), ESplineCoordinateSpace::World, false);

            PointIndex++;
        }
        this->SplineTrack->UpdateSpline();
    }
}*/
