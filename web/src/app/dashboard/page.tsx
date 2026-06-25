import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart3, TrendingUp, Users, DollarSign, Activity } from "lucide-react"

export default function DashboardPage() {
  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Enterprise Command Center</h2>
        <div className="flex items-center space-x-2">
          <div className="text-sm text-muted-foreground bg-muted px-3 py-1 rounded-full">
            Last updated: Just now
          </div>
        </div>
      </div>
      
      {/* KPI Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="glass border-border/50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">₹4,231,890</div>
            <p className="text-xs text-primary font-medium flex items-center mt-1">
              <TrendingUp className="h-3 w-3 mr-1" /> +20.1% from last month
            </p>
          </CardContent>
        </Card>
        <Card className="glass border-border/50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Customers</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">+2,350</div>
            <p className="text-xs text-primary font-medium flex items-center mt-1">
              <TrendingUp className="h-3 w-3 mr-1" /> +180 since last week
            </p>
          </CardContent>
        </Card>
        <Card className="glass border-border/50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Data Health Score</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-primary glow-primary">98.5%</div>
            <p className="text-xs text-muted-foreground mt-1">
              Quality metrics passing
            </p>
          </CardContent>
        </Card>
        <Card className="glass border-border/50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">AI Forecasted Growth</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">+12.5%</div>
            <p className="text-xs text-muted-foreground mt-1">
              Predicted for next quarter
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7 mt-4">
        {/* Main Chart Area */}
        <Card className="col-span-4 glass border-border/50 min-h-[400px] flex flex-col">
          <CardHeader>
            <CardTitle>Revenue Analytics Overview</CardTitle>
          </CardHeader>
          <CardContent className="flex-1 flex items-center justify-center border-t border-border/40 mt-4">
            <div className="text-center space-y-4 text-muted-foreground">
              <BarChart3 className="h-16 w-16 text-border mx-auto" />
              <p>Connect FastAPI backend to render real-time charts here.</p>
            </div>
          </CardContent>
        </Card>

        {/* Secondary Info Area */}
        <Card className="col-span-3 glass border-border/50">
          <CardHeader>
            <CardTitle>Recent Insights</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-8 mt-4">
              <div className="flex items-center">
                <div className="ml-4 space-y-1">
                  <p className="text-sm font-medium leading-none">High-Value Customer Segment Growing</p>
                  <p className="text-sm text-muted-foreground">
                    Segment 'Enterprise Tier' increased by 14% this month.
                  </p>
                </div>
              </div>
              <div className="flex items-center">
                <div className="ml-4 space-y-1">
                  <p className="text-sm font-medium leading-none">Potential Churn Risk Detected</p>
                  <p className="text-sm text-destructive font-medium glow-destructive">
                    3 enterprise clients show reduced activity.
                  </p>
                </div>
              </div>
              <div className="flex items-center">
                <div className="ml-4 space-y-1">
                  <p className="text-sm font-medium leading-none">Data Ingestion Complete</p>
                  <p className="text-sm text-muted-foreground">
                    Salesforce CRM sync finished successfully 2 hours ago.
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
