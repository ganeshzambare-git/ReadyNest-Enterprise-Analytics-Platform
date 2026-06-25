import { Button } from "@/components/ui/button"
import { CheckCircle2 } from "lucide-react"

export default function PricingPage() {
  return (
    <div className="py-24 px-4 sm:px-6 lg:px-8 max-w-screen-xl mx-auto">
      <div className="text-center mb-16">
        <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-4">Simple, transparent pricing</h1>
        <p className="text-xl text-muted-foreground">Choose the plan that fits your enterprise needs.</p>
      </div>

      <div className="grid md:grid-cols-3 gap-8">
        {/* Free Plan */}
        <div className="glass p-8 rounded-2xl border border-border/50 flex flex-col">
          <h3 className="text-2xl font-bold mb-2">Free Plan</h3>
          <p className="text-muted-foreground mb-6">Perfect for exploring the platform.</p>
          <div className="text-4xl font-extrabold mb-8">₹0 <span className="text-lg text-muted-foreground font-normal">/ month</span></div>
          <ul className="space-y-4 mb-8 flex-1">
            <li className="flex items-center"><CheckCircle2 className="h-5 w-5 text-primary mr-3" /> 1 Workspace</li>
            <li className="flex items-center"><CheckCircle2 className="h-5 w-5 text-primary mr-3" /> 1 GB Storage</li>
            <li className="flex items-center"><CheckCircle2 className="h-5 w-5 text-primary mr-3" /> Basic Analytics</li>
            <li className="flex items-center"><CheckCircle2 className="h-5 w-5 text-primary mr-3" /> Basic Reports</li>
          </ul>
          <Button variant="outline" className="w-full">Get Started</Button>
        </div>

        {/* Professional Plan */}
        <div className="glass p-8 rounded-2xl border-2 border-primary relative flex flex-col glow-primary">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-primary text-primary-foreground px-4 py-1 rounded-full text-sm font-semibold tracking-wide">
            MOST POPULAR
          </div>
          <h3 className="text-2xl font-bold mb-2">Professional</h3>
          <p className="text-muted-foreground mb-6">For growing data teams.</p>
          <div className="text-4xl font-extrabold mb-8">₹4,999 <span className="text-lg text-muted-foreground font-normal">/ month</span></div>
          <ul className="space-y-4 mb-8 flex-1">
            <li className="flex items-center"><CheckCircle2 className="h-5 w-5 text-primary mr-3" /> Unlimited Dashboards</li>
            <li className="flex items-center"><CheckCircle2 className="h-5 w-5 text-primary mr-3" /> AI Forecasting</li>
            <li className="flex items-center"><CheckCircle2 className="h-5 w-5 text-primary mr-3" /> Automated Reporting</li>
            <li className="flex items-center"><CheckCircle2 className="h-5 w-5 text-primary mr-3" /> 50 GB Storage</li>
          </ul>
          <Button className="w-full bg-primary text-primary-foreground hover:bg-primary/90">Start Free Trial</Button>
        </div>

        {/* Enterprise Plan */}
        <div className="glass p-8 rounded-2xl border border-border/50 flex flex-col">
          <h3 className="text-2xl font-bold mb-2">Enterprise</h3>
          <p className="text-muted-foreground mb-6">For large scale organizations.</p>
          <div className="text-4xl font-extrabold mb-8">Custom</div>
          <ul className="space-y-4 mb-8 flex-1">
            <li className="flex items-center"><CheckCircle2 className="h-5 w-5 text-primary mr-3" /> RBAC & Row-Level Security</li>
            <li className="flex items-center"><CheckCircle2 className="h-5 w-5 text-primary mr-3" /> SSO Integration</li>
            <li className="flex items-center"><CheckCircle2 className="h-5 w-5 text-primary mr-3" /> Audit Logs</li>
            <li className="flex items-center"><CheckCircle2 className="h-5 w-5 text-primary mr-3" /> Dedicated Support</li>
          </ul>
          <Button variant="outline" className="w-full">Contact Sales</Button>
        </div>
      </div>
    </div>
  )
}
