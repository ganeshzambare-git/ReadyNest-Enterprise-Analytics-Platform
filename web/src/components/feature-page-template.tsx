import * as React from "react"
import { CheckCircle2, ChevronRight, Activity, BarChart3, PieChart, LineChart } from "lucide-react"

export interface FeaturePageProps {
  title: string;
  description: string;
  businessPurpose: string;
  targetUsers: string[];
  useCases: string[];
  capabilities: { title: string; description: string }[];
  benefits: { title: string; description: string }[];
  kpis: { name: string; logic: string }[];
  visualComponents: string[];
}

export function FeaturePageTemplate({
  title,
  description,
  businessPurpose,
  targetUsers,
  useCases,
  capabilities,
  benefits,
  kpis,
  visualComponents
}: FeaturePageProps) {
  return (
    <div className="py-16 md:py-24 px-4 sm:px-6 lg:px-8 max-w-screen-xl mx-auto space-y-24">
      {/* Hero / Overview Section */}
      <section className="text-center space-y-6 max-w-4xl mx-auto">
        <h1 className="text-4xl md:text-6xl font-bold tracking-tight">{title}</h1>
        <p className="text-xl md:text-2xl text-muted-foreground">{description}</p>
        <div className="glass inline-flex p-4 rounded-xl items-center text-left max-w-2xl mt-8">
          <div className="mr-4 text-primary bg-primary/10 p-3 rounded-full">
            <Activity className="h-6 w-6" />
          </div>
          <div>
            <h4 className="font-semibold text-sm uppercase tracking-wide text-primary mb-1">Business Purpose</h4>
            <p className="text-muted-foreground">{businessPurpose}</p>
          </div>
        </div>
      </section>

      <div className="grid md:grid-cols-3 gap-12">
        <div className="md:col-span-2 space-y-24">
          {/* Capabilities Section */}
          <section>
            <h2 className="text-3xl font-bold mb-8">Key Capabilities</h2>
            <div className="grid sm:grid-cols-2 gap-6">
              {capabilities.map((cap, i) => (
                <div key={i} className="glass p-6 rounded-xl border border-border/50">
                  <h3 className="text-xl font-bold mb-2 flex items-center">
                    <CheckCircle2 className="h-5 w-5 text-primary mr-2" />
                    {cap.title}
                  </h3>
                  <p className="text-muted-foreground">{cap.description}</p>
                </div>
              ))}
            </div>
          </section>

          {/* Metrics & KPIs Section */}
          <section>
            <h2 className="text-3xl font-bold mb-8">Metrics & KPIs</h2>
            <div className="overflow-hidden rounded-xl border border-border glass">
              <table className="w-full text-left text-sm">
                <thead className="bg-muted/50 border-b border-border">
                  <tr>
                    <th className="px-6 py-4 font-semibold">Metric Name</th>
                    <th className="px-6 py-4 font-semibold">Calculation Logic</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {kpis.map((kpi, i) => (
                    <tr key={i} className="hover:bg-muted/20 transition-colors">
                      <td className="px-6 py-4 font-medium">{kpi.name}</td>
                      <td className="px-6 py-4 text-muted-foreground">{kpi.logic}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </div>

        <div className="space-y-12">
          {/* Target Users & Use Cases */}
          <section className="glass p-8 rounded-xl border border-border/50">
            <h3 className="text-xl font-bold mb-6">Target Users</h3>
            <ul className="space-y-3 mb-8">
              {targetUsers.map((user, i) => (
                <li key={i} className="flex items-center text-muted-foreground">
                  <ChevronRight className="h-4 w-4 text-primary mr-2" />
                  {user}
                </li>
              ))}
            </ul>
            
            <h3 className="text-xl font-bold mb-6 pt-6 border-t border-border/50">Common Use Cases</h3>
            <ul className="space-y-3">
              {useCases.map((useCase, i) => (
                <li key={i} className="flex items-start text-muted-foreground text-sm">
                  <div className="h-1.5 w-1.5 rounded-full bg-primary mt-1.5 mr-3 flex-shrink-0" />
                  {useCase}
                </li>
              ))}
            </ul>
          </section>

          {/* Business Benefits */}
          <section>
            <h3 className="text-xl font-bold mb-6">Business Benefits</h3>
            <div className="space-y-4">
              {benefits.map((benefit, i) => (
                <div key={i} className="flex">
                  <div className="mr-4 flex-shrink-0">
                    <div className="h-8 w-8 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold">
                      {i + 1}
                    </div>
                  </div>
                  <div>
                    <h4 className="font-semibold">{benefit.title}</h4>
                    <p className="text-sm text-muted-foreground">{benefit.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Suggested Visual Components */}
          <section className="glass p-8 rounded-xl border border-primary/30 glow-primary bg-primary/5">
            <h3 className="text-xl font-bold mb-6 flex items-center">
              <PieChart className="h-5 w-5 text-primary mr-2" />
              Suggested Visuals
            </h3>
            <div className="flex flex-wrap gap-2">
              {visualComponents.map((vc, i) => (
                <span key={i} className="px-3 py-1 rounded-full border border-primary/20 bg-primary/10 text-primary text-xs font-semibold tracking-wide">
                  {vc}
                </span>
              ))}
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}
