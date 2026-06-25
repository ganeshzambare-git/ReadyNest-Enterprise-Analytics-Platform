import Link from "next/link"

export function Footer() {
  return (
    <footer className="border-t border-border/40 bg-background/95">
      <div className="container mx-auto max-w-screen-2xl px-4 md:px-8 py-12 md:py-16">
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-8">
          <div className="col-span-2 lg:col-span-2">
            <Link href="/" className="flex items-center gap-2 mb-4">
              <div className="h-8 w-8 rounded-md bg-primary flex items-center justify-center">
                <span className="font-bold text-primary-foreground leading-none">R</span>
              </div>
              <div className="flex flex-col leading-none">
                <span className="font-bold tracking-tight text-lg">ReadyNest</span>
                <span className="text-[0.65rem] text-muted-foreground uppercase tracking-widest font-semibold">Insight Engine</span>
              </div>
            </Link>
            <p className="text-sm text-muted-foreground max-w-xs mb-6">
              Enterprise Analytics Platform for Data-Driven Organizations. Analyze, understand, predict, and grow.
            </p>
          </div>
          
          <div>
            <h3 className="font-semibold text-sm mb-4">Platform</h3>
            <ul className="flex flex-col gap-2 text-sm text-muted-foreground">
              <li><Link href="/platform/overview" className="hover:text-primary transition-colors">Overview</Link></li>
              <li><Link href="/platform/features" className="hover:text-primary transition-colors">Features</Link></li>
              <li><Link href="/pricing" className="hover:text-primary transition-colors">Pricing</Link></li>
              <li><Link href="/security" className="hover:text-primary transition-colors">Security</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-sm mb-4">Services</h3>
            <ul className="flex flex-col gap-2 text-sm text-muted-foreground">
              <li><Link href="/services/data-foundation" className="hover:text-primary transition-colors">Data Foundation</Link></li>
              <li><Link href="/services/analytics" className="hover:text-primary transition-colors">Analytics & Visuals</Link></li>
              <li><Link href="/services/predictive-ai" className="hover:text-primary transition-colors">Predictive AI</Link></li>
              <li><Link href="/services/governance" className="hover:text-primary transition-colors">Governance</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-sm mb-4">Company</h3>
            <ul className="flex flex-col gap-2 text-sm text-muted-foreground">
              <li><Link href="/about" className="hover:text-primary transition-colors">About</Link></li>
              <li><Link href="/docs" className="hover:text-primary transition-colors">Docs</Link></li>
              <li><Link href="/contact" className="hover:text-primary transition-colors">Contact</Link></li>
              <li><Link href="/careers" className="hover:text-primary transition-colors">Careers</Link></li>
            </ul>
          </div>
        </div>

        <div className="mt-12 pt-8 border-t border-border/40 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-muted-foreground">
            &copy; {new Date().getFullYear()} ReadyNest Insight Engine. All rights reserved.
          </p>
          <div className="flex gap-4 text-sm text-muted-foreground">
            <Link href="/privacy" className="hover:text-primary transition-colors">Privacy Policy</Link>
            <Link href="/terms" className="hover:text-primary transition-colors">Terms of Service</Link>
          </div>
        </div>
      </div>
    </footer>
  )
}
