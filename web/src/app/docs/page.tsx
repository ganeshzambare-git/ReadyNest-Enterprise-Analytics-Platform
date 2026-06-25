import Link from "next/link"

export default function DocsPage() {
  const sections = [
    { title: "Getting Started", href: "/docs/getting-started" },
    { title: "Installation", href: "/docs/installation" },
    { title: "Authentication", href: "/docs/authentication" },
    { title: "Data Ingestion", href: "/docs/data-ingestion" },
    { title: "Data Cleaning", href: "/docs/data-cleaning" },
    { title: "Analytics", href: "/docs/analytics" },
    { title: "Forecasting", href: "/docs/forecasting" },
    { title: "Reporting", href: "/docs/reporting" },
    { title: "Governance", href: "/docs/governance" },
    { title: "Deployment", href: "/docs/deployment" },
    { title: "API Reference", href: "/docs/api-reference" },
    { title: "Troubleshooting", href: "/docs/troubleshooting" },
  ]

  return (
    <div className="flex min-h-screen">
      {/* Docs Sidebar */}
      <aside className="w-64 border-r border-border/40 hidden md:block">
        <div className="h-full py-6 pl-8 pr-6 sticky top-16">
          <h4 className="font-semibold mb-4 text-sm tracking-tight">DOCUMENTATION</h4>
          <ul className="space-y-2 text-sm text-muted-foreground">
            {sections.map((section) => (
              <li key={section.title}>
                <Link href={section.href} className="hover:text-primary transition-colors">
                  {section.title}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </aside>

      {/* Docs Content Placeholder */}
      <main className="flex-1 py-12 px-8 lg:px-16">
        <div className="max-w-3xl prose prose-slate dark:prose-invert">
          <h1>ReadyNest Insight Engine Documentation</h1>
          <p className="text-xl text-muted-foreground">
            Learn how to integrate, analyze, and deploy your enterprise data with our comprehensive guides and API reference.
          </p>
          <hr />
          <h2>Getting Started</h2>
          <p>
            Welcome to the ReadyNest documentation. Choose a topic from the sidebar to begin.
          </p>
        </div>
      </main>
    </div>
  )
}
