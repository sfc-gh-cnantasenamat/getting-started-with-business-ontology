"use client";

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

import { useState } from "react";

interface TabsProps {
  tabs: { id: string; label: string }[];
  children: Record<string, React.ReactNode>;
}

export default function Tabs({ tabs, children }: TabsProps) {
  const [active, setActive] = useState(tabs[0].id);

  return (
    <div>
      <div className="flex gap-1 border-b border-[var(--border)] mb-6">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActive(tab.id)}
            className={`px-5 py-3 text-sm font-medium border-b-2 transition-colors ${
              active === tab.id
                ? "border-[var(--bon)] text-[var(--bon)]"
                : "border-transparent text-[var(--text-muted)] hover:text-[var(--text)]"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div>{children[active]}</div>
    </div>
  );
}
