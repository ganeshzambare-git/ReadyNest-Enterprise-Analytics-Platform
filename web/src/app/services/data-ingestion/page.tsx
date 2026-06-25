import { FeaturePageTemplate } from "@/components/feature-page-template"

export default function DataIngestionPage() {
  return (
    <FeaturePageTemplate 
      title="Data Ingestion"
      description="Seamlessly import, extract, and load data from various enterprise sources into the ReadyNest Data Lake."
      businessPurpose="Centralize disjointed datasets to establish a single source of truth for analytics."
      targetUsers={["Data Engineers","Data Analysts","IT Administrators"]}
      useCases={["Migrating legacy CRM data","Connecting real-time sales APIs","Batch uploading historical Excel reports"]}
      capabilities={[{"title":"CSV & Excel Upload","description":"Drag-and-drop interface for structured flat files."},{"title":"SQL Integration","description":"Direct connection to PostgreSQL, MySQL, and SQL Server databases."},{"title":"API Integration","description":"RESTful endpoints to stream data directly into the lake."},{"title":"Metadata Extraction","description":"Automatically infers schema and data types upon upload."}]}
      benefits={[{"title":"Centralized Data Collection","description":"Eliminates data silos across the organization."},{"title":"Reduced Manual Work","description":"Automates the tedious process of manual data entry and consolidation."}]}
      kpis={[{"name":"Ingestion Volume (GB)","logic":"Total data size uploaded per day."},{"name":"API Error Rate","logic":"Failed API ingestion requests / Total requests."}]}
      visualComponents={["Upload Zone","Dataset Preview Table","Validation Status Cards","Ingestion History Timeline"]}
    />
  )
}
