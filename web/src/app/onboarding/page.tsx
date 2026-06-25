"use client"

import * as React from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { CheckCircle2 } from "lucide-react"

const steps = [
  { id: 1, name: "Create Workspace" },
  { id: 2, name: "Upload Dataset" },
  { id: 3, name: "Configure Analytics" },
  { id: 4, name: "Generate Dashboard" },
  { id: 5, name: "Create First Report" },
]

export default function OnboardingPage() {
  const [currentStep, setCurrentStep] = React.useState(1)
  const router = useRouter()

  const handleNext = () => {
    if (currentStep < steps.length) {
      setCurrentStep((prev) => prev + 1)
    } else {
      router.push("/dashboard")
    }
  }

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep((prev) => prev - 1)
    }
  }

  return (
    <div className="min-h-[calc(100vh-14rem)] bg-muted/30 py-12 px-4 sm:px-6 lg:px-8 flex flex-col items-center">
      <div className="w-full max-w-3xl mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-center mb-6">Welcome to ReadyNest</h1>
        <div className="flex items-center justify-between relative">
          <div className="absolute left-0 top-1/2 -translate-y-1/2 w-full h-1 bg-border -z-10" />
          <div 
            className="absolute left-0 top-1/2 -translate-y-1/2 h-1 bg-primary -z-10 transition-all duration-300" 
            style={{ width: `${((currentStep - 1) / (steps.length - 1)) * 100}%` }}
          />
          {steps.map((step) => (
            <div key={step.id} className="flex flex-col items-center gap-2">
              <div className={`h-10 w-10 rounded-full flex items-center justify-center border-2 transition-colors duration-300 ${
                step.id < currentStep 
                  ? "bg-primary border-primary text-primary-foreground" 
                  : step.id === currentStep 
                  ? "bg-background border-primary text-primary glow-primary" 
                  : "bg-background border-border text-muted-foreground"
              }`}>
                {step.id < currentStep ? <CheckCircle2 className="h-5 w-5" /> : step.id}
              </div>
              <span className="text-xs font-medium hidden sm:block text-muted-foreground">{step.name}</span>
            </div>
          ))}
        </div>
      </div>

      <Card className="w-full max-w-3xl glass border-border/40">
        <CardHeader>
          <CardTitle className="text-2xl">{steps[currentStep - 1].name}</CardTitle>
          <CardDescription>
            {currentStep === 1 && "Let's start by naming your primary analytical workspace."}
            {currentStep === 2 && "Upload your first CSV, Excel, or connect to a database."}
            {currentStep === 3 && "Select the metrics and KPIs you want to track."}
            {currentStep === 4 && "Our Insight Engine is building your personalized dashboard."}
            {currentStep === 5 && "Configure your first automated reporting schedule."}
          </CardDescription>
        </CardHeader>
        <CardContent className="min-h-[200px] flex flex-col justify-center">
          {currentStep === 1 && (
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="workspace">Workspace Name</Label>
                <Input id="workspace" placeholder="e.g., Marketing Analytics" defaultValue="My Enterprise Workspace" />
              </div>
            </div>
          )}
          {currentStep === 2 && (
            <div className="border-2 border-dashed border-border rounded-xl p-12 text-center hover:bg-muted/50 transition-colors cursor-pointer">
              <p className="text-muted-foreground">Drag and drop your files here or click to browse.</p>
              <Button variant="outline" className="mt-4">Select Files</Button>
            </div>
          )}
          {currentStep === 3 && (
            <div className="grid grid-cols-2 gap-4">
              <div className="flex items-center space-x-2 border p-4 rounded-lg cursor-pointer hover:border-primary">
                <input type="checkbox" id="sales" className="rounded text-primary focus:ring-primary" defaultChecked />
                <label htmlFor="sales" className="text-sm font-medium leading-none">Sales Performance</label>
              </div>
              <div className="flex items-center space-x-2 border p-4 rounded-lg cursor-pointer hover:border-primary">
                <input type="checkbox" id="customers" className="rounded text-primary focus:ring-primary" defaultChecked />
                <label htmlFor="customers" className="text-sm font-medium leading-none">Customer Intelligence</label>
              </div>
              <div className="flex items-center space-x-2 border p-4 rounded-lg cursor-pointer hover:border-primary">
                <input type="checkbox" id="forecasting" className="rounded text-primary focus:ring-primary" />
                <label htmlFor="forecasting" className="text-sm font-medium leading-none">AI Forecasting</label>
              </div>
              <div className="flex items-center space-x-2 border p-4 rounded-lg cursor-pointer hover:border-primary">
                <input type="checkbox" id="ops" className="rounded text-primary focus:ring-primary" />
                <label htmlFor="ops" className="text-sm font-medium leading-none">Governance & Ops</label>
              </div>
            </div>
          )}
          {currentStep === 4 && (
            <div className="flex flex-col items-center justify-center space-y-4">
              <div className="h-16 w-16 rounded-full border-4 border-primary border-t-transparent animate-spin" />
              <p className="text-primary font-medium animate-pulse">Generating your dashboard architecture...</p>
            </div>
          )}
          {currentStep === 5 && (
            <div className="space-y-4">
              <div className="space-y-2">
                <Label>Report Frequency</Label>
                <div className="flex gap-4">
                  <Button variant="outline" className="flex-1 hover:border-primary hover:text-primary">Daily</Button>
                  <Button variant="default" className="flex-1 bg-primary text-primary-foreground">Weekly</Button>
                  <Button variant="outline" className="flex-1 hover:border-primary hover:text-primary">Monthly</Button>
                </div>
              </div>
            </div>
          )}
        </CardContent>
        <CardFooter className="flex justify-between border-t border-border/40 pt-6">
          <Button variant="ghost" onClick={handleBack} disabled={currentStep === 1}>
            Back
          </Button>
          <Button onClick={handleNext} className="bg-primary text-primary-foreground hover:bg-primary/90 glow-primary">
            {currentStep === steps.length ? "Finish & Go to Dashboard" : "Continue"}
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}
