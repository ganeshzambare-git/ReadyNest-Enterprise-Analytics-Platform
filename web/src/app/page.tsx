import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ArrowRight, BarChart3, Database, ShieldCheck, Zap } from "lucide-react"

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="relative pt-24 pb-32 lg:pt-36 lg:pb-40 overflow-hidden">
        {/* Abstract Background Elements */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-primary/20 rounded-full blur-[120px] opacity-50 -z-10" />
        <div className="absolute top-0 right-0 w-[400px] h-[400px] bg-accent/20 rounded-full blur-[100px] opacity-30 -z-10" />
        
        <div className="container px-4 md:px-8 mx-auto max-w-screen-2xl text-center">
          <div className="inline-flex items-center rounded-full border border-primary/30 bg-primary/10 px-3 py-1 text-sm font-medium text-primary mb-8 glow-primary">
            <span className="flex h-2 w-2 rounded-full bg-primary mr-2 animate-pulse"></span>
            Enterprise Analytics Platform
          </div>
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 max-w-4xl mx-auto text-foreground">
            Transform Data Into <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">Actionable Business Intelligence</span>
          </h1>
          <p className="text-xl md:text-2xl text-muted-foreground mb-10 max-w-2xl mx-auto">
            ReadyNest Insight Engine empowers organizations to ingest, clean, analyze, visualize, forecast, and govern enterprise data through a unified analytics platform.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/register">
              <Button size="lg" className="h-14 px-8 text-lg bg-primary text-primary-foreground hover:bg-primary/90 glow-primary rounded-full">
                Get Started <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link href="/platform">
              <Button size="lg" variant="outline" className="h-14 px-8 text-lg rounded-full border-border bg-background/50 backdrop-blur-sm hover:bg-accent/10 hover:text-accent transition-all">
                Explore Services
              </Button>
            </Link>
          </div>
        </div>

        {/* Dashboard Visual Placeholder */}
        <div className="mt-20 container mx-auto px-4 md:px-8 max-w-screen-xl">
          <div className="glass rounded-2xl p-4 md:p-8 aspect-[16/9] flex flex-col items-center justify-center text-center relative overflow-hidden border border-white/10 dark:border-white/5">
            <div className="absolute inset-0 bg-gradient-to-t from-background to-transparent z-10" />
            <div className="z-20">
              <BarChart3 className="h-16 w-16 text-primary mx-auto mb-4 animate-bounce" />
              <h3 className="text-2xl font-bold mb-2">Animated Dashboard Visualization</h3>
              <p className="text-muted-foreground">Interactive KPI Cards, Geographic Maps, AI Forecasting, and Executive Reports will be rendered here.</p>
            </div>
            {/* Mock UI Elements */}
            <div className="absolute top-8 left-8 right-8 bottom-8 flex gap-4 opacity-20 -z-0">
              <div className="w-1/4 flex flex-col gap-4">
                <div className="bg-card rounded-lg flex-1 border border-border" />
                <div className="bg-card rounded-lg flex-1 border border-border" />
                <div className="bg-card rounded-lg flex-1 border border-border" />
              </div>
              <div className="w-1/2 bg-card rounded-lg border border-border flex flex-col p-4 gap-4">
                <div className="h-12 bg-muted rounded-md w-full" />
                <div className="flex-1 bg-muted rounded-md w-full" />
              </div>
              <div className="w-1/4 flex flex-col gap-4">
                <div className="bg-card rounded-lg h-1/3 border border-border" />
                <div className="bg-card rounded-lg flex-1 border border-border" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Highlights */}
      <section className="py-24 bg-muted/30">
        <div className="container px-4 md:px-8 mx-auto max-w-screen-2xl">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Analyze. Understand. Predict. Grow.</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">Everything you need to turn raw data into strategic advantage.</p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="glass p-8 rounded-xl flex flex-col items-center text-center transition-transform hover:-translate-y-1 hover:glow-primary cursor-pointer">
              <div className="h-14 w-14 rounded-full bg-primary/20 flex items-center justify-center mb-6 text-primary">
                <Database className="h-7 w-7" />
              </div>
              <h3 className="text-xl font-bold mb-3">Unified Data Foundation</h3>
              <p className="text-muted-foreground">Ingest, clean, and standardize data from any source with automated quality assessments.</p>
            </div>
            <div className="glass p-8 rounded-xl flex flex-col items-center text-center transition-transform hover:-translate-y-1 hover:glow-accent cursor-pointer">
              <div className="h-14 w-14 rounded-full bg-accent/20 flex items-center justify-center mb-6 text-accent">
                <Zap className="h-7 w-7" />
              </div>
              <h3 className="text-xl font-bold mb-3">AI & Predictive Analytics</h3>
              <p className="text-muted-foreground">Forecast revenue, predict customer churn, and generate strategic business suggestions.</p>
            </div>
            <div className="glass p-8 rounded-xl flex flex-col items-center text-center transition-transform hover:-translate-y-1 hover:glow-primary cursor-pointer">
              <div className="h-14 w-14 rounded-full bg-primary/20 flex items-center justify-center mb-6 text-primary">
                <ShieldCheck className="h-7 w-7" />
              </div>
              <h3 className="text-xl font-bold mb-3">Enterprise Governance</h3>
              <p className="text-muted-foreground">Robust RBAC, row-level security, audit logging, and cloud integration built-in.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
