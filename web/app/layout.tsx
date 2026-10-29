/*
 * Copyright 2026 Snowflake Inc.
 * SPDX-License-Identifier: Apache-2.0
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "BON Evaluation — SAP Supply Chain",
  description: "Business Ontology value demonstration with SAP-coded enterprise data",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[var(--bg)] text-[var(--text)] antialiased">
        <header className="border-b border-[var(--border)] bg-[var(--bg-card)]">
          <div className="max-w-7xl mx-auto px-6 py-5">
            <h1 className="text-2xl font-bold tracking-tight">
              Business Ontology Evaluation
            </h1>
            <p className="text-sm text-[var(--text-muted)] mt-1">
              SAP Supply Chain — same well-built semantic views, with and without the Business Ontology. 20 questions across 4 tiers.
            </p>
          </div>
        </header>
        <main className="max-w-7xl mx-auto px-6 py-6">{children}</main>
      </body>
    </html>
  );
}
