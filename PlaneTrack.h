// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
// Imports should be placed above the PlaneTrack.Generated.h line. 
#include <glm/vec3.hpp>
#include "CesiumGeospatial/Ellipsoid.h"
#include "CesiumGeospatial/Cartographic.h"
// Add import paths. Make sure they go above the PlaneTrack.generated.h line
#include "Components/SplineComponent.h"
#include "CesiumGeoreference.h"
#include "Engine/DataTable.h"
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PlaneTrack.generated.h"


USTRUCT(BlueprintType)
struct FAircraftRawData : public FTableRowBase
{
  GENERATED_USTRUCT_BODY()

  public:
    FAircraftRawData()
      : Longitude(0.0)
      , Latitude(0.0)
      , Height(0.0)
    {}

  UPROPERTY(EditAnywhere, Category = "FlightTracker")
    double Longitude;
  UPROPERTY(EditAnywhere, Category = "FlightTracker")
    double Latitude;
  UPROPERTY(EditAnywhere, Category = "FlightTracker")
    double Height;
};



UCLASS()
class CESIUM_ADSB_TEST_API APlaneTrack : public AActor
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	APlaneTrack();

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

public:	
	// Called every frame
	virtual void Tick(float DeltaTime) override;

public: 
  // Spline variable to represent the plane track
  UPROPERTY(BlueprintReadOnly, Category = "FlightTracker")
    USplineComponent* SplineTrack;

  // Cesium class that contain many useful  coordinate conversion functions
  UPROPERTY(EditAnywhere, Category = "FlightTracker")
    ACesiumGeoreference* CesiumGeoreference;

  // An Unreal Engine data table to store the raw flight data
  UPROPERTY(EditAnywhere, Category = "FlightTracker")
    UDataTable* AircraftsRawDataTable;

public:
    // Function to parse the data table and create the spline track
    UFUNCTION(BlueprintCallable, Category = "FlightTracker")
    void LoadSplineTrackPoints();


};
