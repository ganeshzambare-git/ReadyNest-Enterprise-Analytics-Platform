import fs from 'fs';
import path from 'path';

const featuresData = {
  "data-ingestion": {
    title: "Data Ingestion",
    description: "Seamlessly import, extract, and load data from various enterprise sources into the ReadyNest Data Lake.",
    businessPurpose: "Centralize disjointed datasets to establish a single source of truth for analytics.",
    targetUsers: ["Data Engineers", "Data Analysts", "IT Administrators"],
    useCases: ["Migrating legacy CRM data", "Connecting real-time sales APIs", "Batch uploading historical Excel reports"],
    capabilities: [
      { title: "CSV & Excel Upload", description: "Drag-and-drop interface for structured flat files." },
      { title: "SQL Integration", description: "Direct connection to PostgreSQL, MySQL, and SQL Server databases." },
      { title: "API Integration", description: "RESTful endpoints to stream data directly into the lake." },
      { title: "Metadata Extraction", description: "Automatically infers schema and data types upon upload." }
    ],
    benefits: [
      { title: "Centralized Data Collection", description: "Eliminates data silos across the organization." },
      { title: "Reduced Manual Work", description: "Automates the tedious process of manual data entry and consolidation." }
    ],
    kpis: [
      { name: "Ingestion Volume (GB)", logic: "Total data size uploaded per day." },
      { name: "API Error Rate", logic: "Failed API ingestion requests / Total requests." }
    ],
    visualComponents: ["Upload Zone", "Dataset Preview Table", "Validation Status Cards", "Ingestion History Timeline"]
  },
  "data-quality": {
    title: "Data Quality Assessment",
    description: "Evaluate your datasets across critical dimensions to ensure analytical readiness.",
    businessPurpose: "Prevent 'garbage-in, garbage-out' scenarios by catching bad data before it hits the analytics engine.",
    targetUsers: ["Data Stewards", "Data Analysts"],
    useCases: ["Auditing new vendor data", "Checking CRM data completeness"],
    capabilities: [
      { title: "Completeness Score", description: "Measures the percentage of missing values." },
      { title: "Accuracy Score", description: "Validates data against known true values or rules." },
      { title: "Consistency Score", description: "Checks for formatting consistency across columns." }
    ],
    benefits: [
      { title: "Trust in Data", description: "Increases leadership confidence in dashboards." },
      { title: "Early Detection", description: "Catches errors before they corrupt ML models." }
    ],
    kpis: [
      { name: "Overall Quality Score", logic: "Weighted average of Completeness, Accuracy, Validity, Uniqueness." },
      { name: "Missing Values %", logic: "Null records / Total records." }
    ],
    visualComponents: ["Quality Gauge Chart", "Issue Tracker List", "Column Health Bar Chart"]
  },
  "sales-performance": {
    title: "Sales Performance",
    description: "Monitor overall sales effectiveness and identify revenue growth opportunities.",
    businessPurpose: "Provide executives with a real-time view of revenue and sales health.",
    targetUsers: ["VP of Sales", "CRO", "Sales Managers"],
    useCases: ["Quarterly revenue review", "Identifying underperforming regions"],
    capabilities: [
      { title: "Revenue Tracking", description: "Real-time aggregation of all closed-won deals." },
      { title: "Sales Funnel Analysis", description: "Conversion rates between pipeline stages." },
      { title: "Growth Analysis", description: "MoM and YoY growth comparisons." }
    ],
    benefits: [
      { title: "Increased Revenue", description: "Identifies bottlenecks in the sales funnel." },
      { title: "Better Forecasting", description: "Accurate historical data improves future predictions." }
    ],
    kpis: [
      { name: "Total Revenue", logic: "Sum of closed won opportunities." },
      { name: "Average Order Value", logic: "Total Revenue / Number of Orders." }
    ],
    visualComponents: ["Revenue Line Chart", "Sales Funnel", "Growth Waterfall Chart", "KPI Cards"]
  }
};

const basePath = path.join(process.cwd(), 'src', 'app', 'services');

const directories = fs.readdirSync(basePath);

directories.forEach(dir => {
  const dirPath = path.join(basePath, dir);
  if (fs.statSync(dirPath).isDirectory()) {
    const data = featuresData[dir] || {
      title: dir.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '),
      description: "Advanced enterprise module for " + dir.replace(/-/g, ' ') + ".",
      businessPurpose: "Enhance decision making and operational efficiency.",
      targetUsers: ["Business Analysts", "Executives", "Data Scientists"],
      useCases: ["Enterprise reporting", "Strategic planning", "Operational monitoring"],
      capabilities: [
        { title: "Advanced Analytics", description: "Deep dive into your metrics." },
        { title: "Real-time Processing", description: "Data processed with sub-second latency." }
      ],
      benefits: [
        { title: "ROI Improvement", description: "Direct impact on bottom line." },
        { title: "Time Savings", description: "Automates manual analysis workflows." }
      ],
      kpis: [
        { name: "Usage Rate", logic: "Active Users / Total Licensed Users" },
        { name: "Time to Insight", logic: "Time from data ingestion to dashboard render" }
      ],
      visualComponents: ["Interactive Charts", "Data Tables", "KPI Scorecards", "Geographic Maps"]
    };

    const componentName = data.title.replace(/\s+/g, '').replace(/&/g, 'And');

    const content = `import { FeaturePageTemplate } from "@/components/feature-page-template"

export default function ${componentName}Page() {
  return (
    <FeaturePageTemplate 
      title=${JSON.stringify(data.title)}
      description=${JSON.stringify(data.description)}
      businessPurpose=${JSON.stringify(data.businessPurpose)}
      targetUsers={${JSON.stringify(data.targetUsers)}}
      useCases={${JSON.stringify(data.useCases)}}
      capabilities={${JSON.stringify(data.capabilities)}}
      benefits={${JSON.stringify(data.benefits)}}
      kpis={${JSON.stringify(data.kpis)}}
      visualComponents={${JSON.stringify(data.visualComponents)}}
    />
  )
}
`;
    
    fs.writeFileSync(path.join(dirPath, 'page.tsx'), content);
    console.log("Updated feature page: " + dir);
  }
});
