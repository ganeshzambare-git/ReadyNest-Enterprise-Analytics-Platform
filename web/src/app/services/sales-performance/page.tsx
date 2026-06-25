import { FeaturePageTemplate } from "@/components/feature-page-template"

export default function SalesPerformancePage() {
  return (
    <FeaturePageTemplate 
      title="Sales Performance"
      description="Monitor overall sales effectiveness and identify revenue growth opportunities."
      businessPurpose="Provide executives with a real-time view of revenue and sales health."
      targetUsers={["VP of Sales","CRO","Sales Managers"]}
      useCases={["Quarterly revenue review","Identifying underperforming regions"]}
      capabilities={[{"title":"Revenue Tracking","description":"Real-time aggregation of all closed-won deals."},{"title":"Sales Funnel Analysis","description":"Conversion rates between pipeline stages."},{"title":"Growth Analysis","description":"MoM and YoY growth comparisons."}]}
      benefits={[{"title":"Increased Revenue","description":"Identifies bottlenecks in the sales funnel."},{"title":"Better Forecasting","description":"Accurate historical data improves future predictions."}]}
      kpis={[{"name":"Total Revenue","logic":"Sum of closed won opportunities."},{"name":"Average Order Value","logic":"Total Revenue / Number of Orders."}]}
      visualComponents={["Revenue Line Chart","Sales Funnel","Growth Waterfall Chart","KPI Cards"]}
    />
  )
}
