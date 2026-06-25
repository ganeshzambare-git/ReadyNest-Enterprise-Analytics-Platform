"use client"

import * as React from "react"
import Link from "next/link"
import { cn } from "@/lib/utils"
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu"

const dataFoundation = [
  { title: "Data Ingestion", href: "/services/data-ingestion", description: "Seamlessly import data from multiple sources." },
  { title: "Data Quality Assessment", href: "/services/data-quality", description: "Evaluate completeness, accuracy, and validity." },
  { title: "Data Cleaning", href: "/services/data-cleaning", description: "Handle missing values, outliers, and duplicates." },
  { title: "Descriptive Statistics", href: "/services/descriptive-statistics", description: "Core metrics like mean, variance, and standard deviation." },
  { title: "Univariate Analysis", href: "/services/univariate-analysis", description: "Histograms, box plots, and density plots." },
  { title: "Bivariate Analysis", href: "/services/bivariate-analysis", description: "Scatter plots and correlation matrices." },
]

const customerIntelligence = [
  { title: "Customer Overview", href: "/services/customer-overview", description: "360-degree view of total and active customers." },
  { title: "Customer Analysis", href: "/services/customer-analysis", description: "Analyze behavior, CLV, and retention metrics." },
  { title: "Customer Segmentation", href: "/services/customer-segmentation", description: "RFM segmentation and high-value customer identification." },
]

const salesAndProduct = [
  { title: "Sales Performance", href: "/services/sales-performance", description: "Revenue tracking and profitability analysis." },
  { title: "Product Performance", href: "/services/product-performance", description: "Evaluate best-selling and risky products." },
]

const businessIntelligence = [
  { title: "Behavior Analysis", href: "/services/behavior-analysis", description: "Purchase patterns and journey tracking." },
  { title: "Key Insights", href: "/services/key-insights", description: "AI-generated findings and trend detection." },
  { title: "Business Suggestions", href: "/services/business-suggestions", description: "Actionable recommendations based on data." },
]

export function MainNav() {
  return (
    <div className="flex flex-1 items-center gap-6">
      <Link href="/" className="flex items-center gap-2">
        <div className="h-8 w-8 rounded-md bg-primary flex items-center justify-center">
          <span className="font-bold text-primary-foreground leading-none">R</span>
        </div>
        <div className="flex flex-col leading-none">
          <span className="font-bold tracking-tight text-lg">ReadyNest</span>
          <span className="text-[0.65rem] text-muted-foreground uppercase tracking-widest font-semibold">Insight Engine</span>
        </div>
      </Link>
      <div className="hidden md:flex">
        <NavigationMenu>
          <NavigationMenuList>
          <NavigationMenuItem>
            <Link href="/platform" legacyBehavior passHref>
              <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                Platform
              </NavigationMenuLink>
            </Link>
          </NavigationMenuItem>
          <NavigationMenuItem>
            <NavigationMenuTrigger>Services</NavigationMenuTrigger>
            <NavigationMenuContent>
              <div className="grid w-[800px] grid-cols-4 gap-4 p-4 md:w-[900px] lg:w-[1000px]">
                <div className="col-span-1">
                  <h4 className="mb-2 text-sm font-semibold tracking-tight text-primary uppercase">Data Foundation</h4>
                  <ul className="flex flex-col gap-1">
                    {dataFoundation.map((item) => (
                      <ListItem key={item.title} title={item.title} href={item.href} />
                    ))}
                  </ul>
                </div>
                <div className="col-span-1">
                  <h4 className="mb-2 text-sm font-semibold tracking-tight text-primary uppercase">Customer Intel</h4>
                  <ul className="flex flex-col gap-1">
                    {customerIntelligence.map((item) => (
                      <ListItem key={item.title} title={item.title} href={item.href} />
                    ))}
                  </ul>
                  <h4 className="mt-4 mb-2 text-sm font-semibold tracking-tight text-primary uppercase">Sales & Product</h4>
                  <ul className="flex flex-col gap-1">
                    {salesAndProduct.map((item) => (
                      <ListItem key={item.title} title={item.title} href={item.href} />
                    ))}
                  </ul>
                </div>
                <div className="col-span-1">
                  <h4 className="mb-2 text-sm font-semibold tracking-tight text-primary uppercase">Business Intel</h4>
                  <ul className="flex flex-col gap-1">
                    {businessIntelligence.map((item) => (
                      <ListItem key={item.title} title={item.title} href={item.href} />
                    ))}
                  </ul>
                  <h4 className="mt-4 mb-2 text-sm font-semibold tracking-tight text-primary uppercase">Analytics & AI</h4>
                  <ul className="flex flex-col gap-1">
                    <ListItem title="Interactive Dashboard" href="/services/interactive-dashboard" />
                    <ListItem title="Predictive Modeling" href="/services/predictive-modeling" />
                    <ListItem title="Advanced Visuals" href="/services/advanced-visuals" />
                  </ul>
                </div>
                <div className="col-span-1">
                  <h4 className="mb-2 text-sm font-semibold tracking-tight text-primary uppercase">Ops & Reporting</h4>
                  <ul className="flex flex-col gap-1">
                    <ListItem title="Automated Reporting" href="/services/automated-reporting" />
                    <ListItem title="Governance & Security" href="/services/governance-security" />
                    <ListItem title="Monitoring & Ops" href="/services/monitoring-observability" />
                    <ListItem title="Cloud Integration" href="/services/cloud-integration" />
                  </ul>
                </div>
              </div>
            </NavigationMenuContent>
          </NavigationMenuItem>
          <NavigationMenuItem>
            <Link href="/resources" legacyBehavior passHref>
              <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                Resources
              </NavigationMenuLink>
            </Link>
          </NavigationMenuItem>
          <NavigationMenuItem>
            <Link href="/pricing" legacyBehavior passHref>
              <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                Pricing
              </NavigationMenuLink>
            </Link>
          </NavigationMenuItem>
          <NavigationMenuItem>
            <Link href="/docs" legacyBehavior passHref>
              <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                Docs
              </NavigationMenuLink>
            </Link>
          </NavigationMenuItem>
          <NavigationMenuItem>
            <Link href="/about" legacyBehavior passHref>
              <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                About
              </NavigationMenuLink>
            </Link>
          </NavigationMenuItem>
        </NavigationMenuList>
      </NavigationMenu>
      </div>
    </div>
  )
}

const ListItem = React.forwardRef<
  React.ElementRef<"a">,
  React.ComponentPropsWithoutRef<"a">
>(({ className, title, children, ...props }, ref) => {
  return (
    <li>
      <NavigationMenuLink
        ref={ref}
        className={cn(
          "block select-none space-y-1 rounded-md p-2 leading-none no-underline outline-none transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
          className
        )}
        {...props}
      >
        <div className="text-sm font-medium leading-none">{title}</div>
        {children && (
          <p className="line-clamp-2 text-xs leading-snug text-muted-foreground mt-1">
            {children}
          </p>
        )}
      </NavigationMenuLink>
    </li>
  )
})
ListItem.displayName = "ListItem"
