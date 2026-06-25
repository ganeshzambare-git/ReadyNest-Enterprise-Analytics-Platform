import { FeaturePageTemplate } from "@/components/feature-page-template"

export default function DataQualityAssessmentPage() {
  return (
    <FeaturePageTemplate 
      title="Data Quality Assessment"
      description="Evaluate your datasets across critical dimensions to ensure analytical readiness."
      businessPurpose="Prevent 'garbage-in, garbage-out' scenarios by catching bad data before it hits the analytics engine."
      targetUsers={["Data Stewards","Data Analysts"]}
      useCases={["Auditing new vendor data","Checking CRM data completeness"]}
      capabilities={[{"title":"Completeness Score","description":"Measures the percentage of missing values."},{"title":"Accuracy Score","description":"Validates data against known true values or rules."},{"title":"Consistency Score","description":"Checks for formatting consistency across columns."}]}
      benefits={[{"title":"Trust in Data","description":"Increases leadership confidence in dashboards."},{"title":"Early Detection","description":"Catches errors before they corrupt ML models."}]}
      kpis={[{"name":"Overall Quality Score","logic":"Weighted average of Completeness, Accuracy, Validity, Uniqueness."},{"name":"Missing Values %","logic":"Null records / Total records."}]}
      visualComponents={["Quality Gauge Chart","Issue Tracker List","Column Health Bar Chart"]}
    />
  )
}
