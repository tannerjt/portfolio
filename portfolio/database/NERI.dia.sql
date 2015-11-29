-- Author : Joshua Tanner
-- UnitID : jmtanne2

-- Create Tables
create table lu_species (
   SpeciesID     varchar (255) not null,--  Unique identification code assigned to the species.   " Zero" = no animal observed
   CategoryID    integer               ,--  Code indicating whether the species is mammal (500), reptile (530), or amphibian (540)
   FullLatinName varchar (255)         ,--  Full Latin name of the species
   CommonName    varchar (255)         ,--  Common name of the species
   constraint pk_lu_species primary key (SpeciesID)
)   ;
create table tbl_data (
   RecID      integer       not null,--  Unique number automatically assigend to each record to prevent duplicates in key fields
   LocationID varchar (255)         ,--  Identification code of the sampling location where the species was observed
   EventID    varchar (255)         ,--  Identification code of  the sampling event during which the species was observed
   Category   integer               ,--  Type of animal observed: 10=frog; 20=salamander; 30=lizard; 40=turtle; 50=snake; 60=mammal; 80=no animal observed
   Protocol   varchar (255)         ,--  Sampling method used
   SpeciesID  varchar (255)         ,--  Species identification code of the animal observed.  "Zero"=no animal observed.
   TimeofDay  varchar (255)         ,--  Indicates whether animal was observed during the day or at night
   Number     integer               ,--  Number of individuals captured (25="several" in field notes;15="numerous" in field notes)
   constraint pk_tbl_data primary key (RecID)
)   ;
create table tblEvents (
   EventID varchar (255) not null,--  Identification code of the sampling event
   Year    integer               ,--  Year in which the sampling event occurred
   constraint pk_tblEvents primary key (EventID)
)   ;
create table tblLocations (
   LocationID         varchar (255)  not null,--  Unique identification code assigned to the sampling location
   LocationDescript   varchar (255)          ,--  Description of the location (<256 characters)
   UTMX               numeric (15,2)         ,--  UTM X (easting) coordinate for the center of the plot or location OR starting point of a line or polygon (double precision to15 significant digits)
   UTMY               numeric (15,2)         ,--  UTM Y (northing) coordinate for the center of the plot or location OR starting point of a line or polygon (double precision to15 significant digits)
   Habitat            varchar (255)          ,--  Habitat type (aquatic or terrestrial)
   HabitatDescription varchar (255)          ,--  Description of habitat
   constraint pk_tblLocations primary key (LocationID)
)   ;


-- Define Keys
alter table tbl_data add constraint dataHasSpecies 
    foreign key (SpeciesID)
    references lu_species (SpeciesID) ;
alter table tbl_data add constraint dataHasEvents 
    foreign key (EventID)
    references tblEvents (EventID) ;
alter table tbl_data add constraint dataHasLocations 
    foreign key (LocationID)
    references tblLocations (LocationID) ;
