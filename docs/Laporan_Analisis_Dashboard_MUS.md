# EVALUASI KRITIS: Montana University System (MUS) Dual Enrollment Dashboards

### Nama : Muhammad Dhiauddin

### NIM : 25917024

### Program : Magister Teknik Informatika

### Konsentrasi : Sains Data Profesional

---

## A. ANALISIS PENGGUNA (User Analysis)

### 1. Identifikasi Pengguna Utama dan Alasan

Berdasarkan konten dan fokus data yang ditampilkan, dashboard MUS dirancang terutama untuk:

#### a) Administrator dan Policy Makers (Rektorat/Sistem Level Management)

- **Alasan:** Dashboard menampilkan data agregat sistem-wide (total enrollment, year-over-year growth rates, institutional breakdown). Fokus pada trend jangka panjang dan perbandingan antar institusi menunjukkan kebutuhan untuk strategic planning dan resource allocation.
- **Contoh:** Grafik "MUS Dual Enrollment Matriculation by Institution" menampilkan total sistem (7,620 hingga 8,071 students), memungkinkan eksekutif untuk mengidentifikasi institusi mana yang berkontribusi paling besar terhadap dual enrollment success.

#### b) Academic Program Directors dan Dual Enrollment Coordinators

- **Alasan:** Dashboard menyediakan data spesifik tentang modalitas pembelajaran, tipe kredit, dan institusi penerima mahasiswa. Ini penting untuk program coordination dan curriculum planning.
- **Contoh:** Dashboard "Dual Enrollment Modality and Credit Type" menunjukkan bahwa "In-Person Concurrent Enrollment" mendominasi (39,606 credit hours pada tahun 24-25), sementara "Online Early College" meningkat signifikan (10,874 credit hours). Coordinator dapat menggunakan insight ini untuk menentukan resource allocation dan infrastructure needs.

#### c) High School Partnership Officers dan District Administrators

- **Alasan:** Dashboard menampilkan geographic data (county-level, high school district, individual high schools) yang memudahkan identifikasi partnership opportunities dan performance monitoring.
- **Contoh:** "County and High School Dual Enrollment Counts" menunjukkan distribusi geografis dengan stars menandai high schools utama. District administrator dapat melihat mana schools yang paling aktif dan mana yang memiliki potensi untuk ditingkatkan.

#### d) Institutional Research Offices

- **Alasan:** Data longitudinal (12-13 hingga 24-25) memungkinkan analisis trend, cohort tracking, dan effectiveness measurement dari dual enrollment programs.

### 2. Contoh Spesifik Pengambilan Keputusan

| Pertanyaan Pengguna                          | Informasi dari Dashboard                                                                                     | Keputusan yang Mungkin                                                                                        |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| Apakah program DE kita tumbuh?               | Growth rates year-over-year: 26.34% (13-14), 16.97% (14-15), mencapai 11.36% (24-25)                         | Keputusan untuk meningkatkan marketing dan expansion efforts karena pertumbuhan melambat                      |
| Modality mana yang paling efektif?           | In-Person Concurrent (39,606 jam) >> Online Early College (10,874 jam)                                       | Prioritas untuk mempertahankan program in-person sambil mengembangkan online infrastructure                   |
| Institusi mana yang top performers?          | City College dan Flathead Valley CC menunjukkan enrollment tertinggi                                         | Resource allocation untuk supporting high-performing institutions dan benchmarking untuk lagging institutions |
| Dari mana siswa DE berasal secara geografis? | Map dan district table menunjukkan konsentrasi di urban areas (Missoula dengan 7,511, Billings dengan 4,971) | Expansion strategy dapat fokus pada rural areas yang underrepresented atau underutilized                      |

---

## B. EVALUASI UX/UI DAN FITUR

### 1. Analisis Usability (Kemudahan/Kesulitan Penggunaan)

#### Kekuatan (+)

- **Filter interaktif yang jelas:** Dropdown "Year," "DE Campus," dan "HS Type" memungkinkan user untuk menyelam ke level detail tertentu tanpa overwhelming dengan informasi.
- **Multiple visualization perspectives:** Kombinasi bar charts, line graphs, dan maps memberikan berbagai cara untuk memahami data yang sama.
- **Logical information hierarchy:** Dashboard diorganisir dari overview (total enrollment trends) menuju specific breakdowns (by modality, campus, geographic).

#### Kelemahan (-)

- **Terlalu banyak dashboard pages:** Dengan 8 dashboard berbeda, user perlu untuk memilih atau navigate antar-dashboard untuk mendapatkan complete picture. Ini bisa menyebabkan **cognitive overload** dan requires prior knowledge tentang struktur program.
- **Limited contextual guidance:** Dashboard description singkat, namun kurang penjelasan tentang _mengapa_ metrik tertentu penting atau _bagaimana_ menginterpretasi data anomali (contoh: dip pada tahun 20-21 tidak dijelaskan).
- **Data masking transparency:** Beberapa dashboard mencatat "counts under 5 have been masked" untuk privacy, tetapi user tidak tahu bagaimana ini mempengaruhi analisis keseluruhan atau aggregate figures.
- **Dashboard interdependency confusion:** Tidak jelas hubungan logis antara "Institutional Matriculation" (menampilkan students di City College, MSU-Billings) versus "MUS DE Matriculation by Institution" (menampilkan students yang masuk ke MUS sistem).

### 2. Efektivitas Visualisasi Data

| Visualisasi                                            | Efektivitas    | Analisis                                                                                                                                                                                                        |
| ------------------------------------------------------ | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Bar Chart + Line Graph (Enrollment & Credit Hours)** |  BAIK        | Dual-axis visualization sangat efektif untuk menunjukkan relationship antara enrollment count dan average credit hours. Pola jelas: enrollment growth correlates dengan consistent credit hours attempted (~6). |
| **Stacked Area Chart (Modality & Credit Type)**        |  BAIK        | Memudahkan melihat composition changes (in-person vs online) seiring waktu. Warna-warna distinct dan legend jelas.                                                                                              |
| **Stacked Bar Chart (Matriculation by Institution)**   |  SEDANG      | Efektif untuk menunjukkan composition, tetapi sulit untuk membaca nilai absolut institusi individual. Ada ~10+ institusi, membuat lebih dari 10 color categories—potentially confusing.                         |
| **Sankey Diagram (HS → DE → MUS Pathways)**            |  SANGAT BAIK | Excellent untuk menunjukkan complex flow dan relationships. Visualisasi ini memungkinkan tracking pathway dari 40+ high schools → ~10 DE campuses → ultimate MUS institution.                                   |
| **Geographic Maps (County & District)**                |  BAIK        | Color intensity scale (light = fewer students, dark = more students) intuitif. Stars untuk highlight key institutions. Map context membantu stakeholders dari berbagai counties.                                |
| **Data Tables (Detailed Numbers)**                     |  BAIK        | Comprehensive dan accurate. Memungkinkan drill-down dari visualization ke raw numbers.                                                                                                                          |

**Catatan Kritis:**

- Visualisasi over-relying pada color differentiation (8+ colors) dapat problematic untuk colorblind users.
- Line graphs sangat sulit dibaca ketika ada 10+ lines (contoh: Campus DE Counts line graph). Y-axis readability berkurang.

### 3. Fitur-Fitur Interaktif

| Fitur                              | Deskripsi                                                         | Manfaat                                                                          | Limitasi                                                                                           |
| ---------------------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Year Selector (Dropdown)**       | Memilih single year atau "All years"                              | Memungkinkan year-over-year comparison dan longitudinal analysis (13 tahun data) | Tidak ada date range slider—user harus memilih single year                                         |
| **DE Campus Filter**               | Dropdown untuk memilih specific dual enrollment campus atau "All" | Koordinator dapat fokus pada performance specific campus untuk action planning   | Filter placement berbeda antar dashboard—inconsistent UX                                           |
| **HS Type / HS Name Filter**       | Kategori untuk high school type atau individual school selection  | Geographic focus membantu partnership officers                                   | Ketika dipilih institutional specific filters, beberapa aggregate numbers berubah—perlu penjelasan |
| **Hover Tooltips (assumed)**       | Data point details on hover                                       | Contextual info tanpa cluttering visualization                                   | Tidak terlihat jelas dalam static images—assumed feature based on modern BI tools                  |
| **Legend Interactivity (assumed)** | Click legend items to toggle series on/off                        | Reduce visual clutter, highlight specific categories                             | Limited evident from static views                                                                  |

**Kesimpulan Fitur:** Interaktivitas ada tetapi masih basic level. Tidak ada advanced analytics seperti predictive trends, anomaly detection, atau correlation analysis.

---

## C. ANALISIS KONTEN (Data Content Analysis)

### 1. Data/Informasi yang Ditampilkan

#### Dashboard 1: MUS Dual Enrollment Counts

- Enrollment counts (13 tahun, 1,735 → 9,071 students)
- Year-over-year growth rates (range: -5.89% to 29.02%)
- Average hours attempted & earned per student (trend relatively stable ~6 hours)

#### Dashboard 2: Dual Enrollment Modality and Credit Type

- Credit hours by modality: In-person concurrent, Early college, Online
- Credit type breakdown: Concurrent (high school + college) vs Early college (college only)
- 6 distinct modality/credit combinations tracked

#### Dashboard 3: Campus Dual Enrollment Counts

- Per-institution enrollment breakdown (10 institutions tracked)
- Term-level granularity (Fall, Spring, Summer)
- 13-year institutional trends

#### Dashboard 4: HS to DE to MUS Enrollment Pathways

- Complex sankey showing 40+ high schools → 10 DE campuses → MUS matriculation campuses
- Cohort tracking dari HS enrollment hingga eventual MUS enrollment

#### Dashboard 5: County & High School DE Counts

- Geographic heat map (county-level) dengan 56 counties
- Individual high school enumeration (90+ schools tracked)
- County aggregates not equal to school sums (masking effect)

#### Dashboard 6: Institutional Matriculation

- Students who took DE at specific institution (City College example)
- Their matriculation to MUS campuses
- Breakdown by major field dan incoming DE courses

#### Dashboard 7: MUS DE Matriculation by Institution

- System-wide matriculation targets (12 MUS institutions)
- Enrollment status: "No MUS Enrollment" vs. matriculated to specific institution
- Major breakdowns (Accounting, Administrative roles, etc.)

#### Dashboard 8: High School District DE Counts

- Public school district aggregation (~80 districts)
- District-level trends over 13 years
- Map visualization dengan district boundaries

### 2. Data/Informasi yang Seharusnya Ditambahkan (Recommendations)

#### a) Retention & Success Metrics

- **Gap:** Dashboard melacak enrollment dan matriculation, tetapi tidak ada data tentang course completion rates, GPA, atau degree attainment dari DE students.
- **Rekomendasi:** Tambahkan completion rates per course type (concurrent vs. early college) dan time-to-degree analysis. Ini penting untuk measuring program effectiveness bukan hanya enrollment growth.
- **Contoh Metric:** "DE Student Completion Rates by Course Type" dengan breakdown untuk melihat apakah concurrent students lebih sukses vs. early college students.

#### b) Cost-Benefit Analysis

- **Gap:** Tidak ada informasi tentang program costs, cost per student, atau ROI dari DE program.
- **Rekomendasi:** Dashboard untuk program costs (instructional costs, platform fees untuk online) dan cost per credit hour by modality.
- **Contoh Metric:** "Cost per DE Credit Hour by Modality" untuk justifikasi investment dalam online infrastructure.

#### c) Demographics & Equity

- **Gap:** Data tidak terpilah berdasarkan demographics (race/ethnicity, gender, first-generation status, SES). Ini crucial untuk assessing equity in program access.
- **Rekomendasi:** Add demographic breakdown dashboard untuk monitoring underrepresented group participation.
- **Contoh Metric:** "DE Enrollment by Demographic Category" dengan equity gap analysis.

#### d) College Readiness Indicators

- **Gap:** Tidak ada data tentang college readiness assessment scores atau relationship antara DE participation dan later academic performance di college.
- **Rekomendasi:** Link DE data dengan college placement test scores, prerequisite waiver rates, atau college GPA distributions.
- **Contoh Metric:** "Average College GPA by DE Status" untuk mengukur whether DE participation leads ke better college preparation.

#### e) Faculty & Instructor Data

- **Gap:** Dashboard fokus pada student outcomes tetapi tidak menampilkan instructor qualifications, course standardization, atau quality consistency across institutions.
- **Rekomendasi:** Add instructor metrics dashboard.
- **Contoh Metric:** "Instructor Credentials by Institution" dan "Course Alignment Assessment Scores" untuk quality assurance.

#### f) Comparative Analysis

- **Gap:** Tidak ada benchmarking dengan state atau national DE program averages.
- **Rekomendasi:** Tambahkan national comparison data untuk kontekstualisasi Montana performance.
- **Contoh Metric:** "MUS DE Participation Rate vs. National Average DE Programs."

#### g) Predictive Analytics

- **Gap:** All data retrospective. Tidak ada forecasting untuk future demand atau scenario planning.
- **Rekomendasi:** Predictive models untuk enrollment forecasting dan resource planning.

#### h) Student Feedback & Satisfaction

- **Gap:** Tidak ada qualitative data atau satisfaction surveys dari students atau high school partners.
- **Rekomendasi:** Dashboard untuk survey results tentang program quality dan student satisfaction.

#### i) Detailed Breakdowns by Subject/Discipline

- **Gap:** Hanya "Matriculated Majors" ditampilkan untuk one institution. Tidak ada discipline-level analysis across all DE programs.
- **Rekomendasi:** "DE Enrollment by Discipline/Subject" dashboard untuk understanding curriculum distribution dan demand patterns.

---

## RINGKASAN EVALUASI DASHBOARD MUS

### Kekuatan Utama

1. **Comprehensive longitudinal data** (13 tahun)
2. **Multiple perspectives** (institutional, geographic, modality, pathway)
3. **Complex relationships well-visualized** (sankey diagram)
4. **Interactive filtering** untuk drill-down analysis
5. **Clear documentation** dengan descriptive text

### Kelemahan Utama

1. **Fragmentasi ke 8 separate dashboards** — burdensome for holistic view
2. **Limited explanatory context dan guidance** untuk interpretation
3. **Fokus heavily pada enrollment metrics** — minimal pada success/outcome metrics
4. **Tidak ada equity analysis** atau demographic breakdowns
5. **Cost-benefit analysis completely absent**
6. **UX inconsistency** across multiple dashboards

### Penilaian Keseluruhan

| Aspek                 | Skor | Keterangan                                                                                                    |
| --------------------- | ---- | ------------------------------------------------------------------------------------------------------------- |
| **Usability**         | 7/10 | Functional dan informative tetapi bisa lebih streamlined dan user-centric.                                    |
| **Data Completeness** | 6/10 | Comprehensive dalam tracking enrollment tetapi gaps significant dalam success metrics, equity, dan cost data. |
| **Visual Design**     | 7/10 | Generally baik, tetapi ada issues dengan color differentiation dan line chart readability.                    |
| **Interactivity**     | 6/10 | Basic filtering ada, tetapi limited advanced analytics capabilities.                                          |
| **Strategic Value**   | 8/10 | Sangat valuable untuk institutional decision-making dan strategic planning.                                   |

### Kesimpulan Akhir

Dashboard MUS Dual Enrollment adalah **sistem informasi yang komprehensif dan strategis** untuk tracking program performance dan institutional relationships. Namun, dashboard ini masih **memiliki ruang signifikan untuk improvement** dalam hal user experience integration, success metrics completeness, dan equity analysis. Untuk maksimal utility, rekomendasi adalah:

1. **Consolidate dashboards** ke dalam unified interface dengan clear navigation
2. **Tambahkan contextual help** dan interpretive guidance
3. **Integrate success metrics** (completion, GPA, time-to-degree)
4. **Add equity analytics** untuk tracking underrepresented populations
5. **Include cost-benefit analysis** untuk program justification dan ROI

---

_Evaluasi ini disusun berdasarkan analisis akademis dari 8 dashboard views Montana University System Dual Enrollment Program._
