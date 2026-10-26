/*!
 * WebMCP tool registrations for timursalakhetdinov.com.
 * Exposes read-only tools so AI agents, recruiter bots, and collaborator-
 * seeking agents can query Timur Salakhetdinov's profile, skills,
 * experience, projects, hiring status, and contact details.
 * Spec: https://developer.chrome.com/docs/ai/webmcp/imperative-api
 */
(function () {
  'use strict';

  if (window.__tsWebMcpRegistered) {
    return;
  }

  var mc = document.modelContext || navigator.modelContext || window.modelContext;
  if (!mc || typeof mc.registerTool !== 'function') {
    return;
  }

  window.__tsWebMcpRegistered = true;

  var SITE_URL = 'https://timursalakhetdinov.com/';
  var CV_URL = 'https://timursalakhetdinov.com/cv.pdf';
  var CV_URL_DE = 'https://timursalakhetdinov.com/cv-de.pdf';

  var DATA = {
    profile: {
      name: 'Timur Salakhetdinov',
      headline: 'Data Scientist & Data Analyst in Germany (Berlin · Hamburg · Munich)',
      summary: 'Data Scientist & Data Analyst specialising in analytics engineering, foundation model forecasting, and LLM agent systems. Currently a Working Student in Analytics at InnoGames in Hamburg, testing Microsoft Fabric for analytics workflows, plus funnel and A/B-test analysis. In parallel, my company project and M.Sc. thesis at Leuphana University forecasts each game\'s daily net revenue over a 90-day horizon as daily active users times revenue per daily active user, using two frozen foundation models (TabPFN-TS and Chronos-2) with calendar features and no task-specific training, and tests agent-compiled planning-text covariates against a shuffled-text placebo. I bring ten years of analytics experience across gaming, telecommunications, finance, and insurance.',
      currentRole: 'Working Student, Analytics at InnoGames (Hamburg, hybrid), since November 2025',
      education: 'M.Sc. Management & Data Science, Leuphana Universität Lüneburg (2024–27, expected March 2027), GPA 1.9 (German scale, 1.0 = best), Deutschlandstipendium scholar',
      availability: 'Available for full-time Data Scientist or Data Analyst roles in Germany from April 2027',
      location: 'Hamburg, Germany',
      languages: [
        { name: 'English', level: 'C1 · IELTS 8.0' },
        { name: 'German', level: 'B2' },
        { name: 'Russian', level: 'Native' }
      ],
      siteUrl: SITE_URL,
      cvUrl: CV_URL,
      cvUrlDe: CV_URL_DE
    },

    skills: {
      proficiencyScale: 'Self-assessed proficiency, 1-5 dots as shown on the site',
      groups: [
        {
          group: 'Languages',
          skills: [
            { name: 'Python (NumPy, Pandas, Scikit-Learn)', proficiency: 5 },
            { name: 'SQL (MS SQL Server, Hive, StarRocks)', proficiency: 5 }
          ]
        },
        {
          group: 'LLM & Agents',
          skills: [
            { name: 'LangGraph', proficiency: 4 },
            { name: 'Coding agents', proficiency: 5 },
            { name: 'MCP', proficiency: 4 },
            { name: 'Tool calling', proficiency: 4 },
            { name: 'RAG', proficiency: 4 }
          ]
        },
        {
          group: 'ML & Forecasting',
          skills: [
            { name: 'TabPFN', proficiency: 5 },
            { name: 'Chronos', proficiency: 4 },
            { name: 'TimesFM', proficiency: 4 },
            { name: 'LightGBM', proficiency: 4 },
            { name: 'PyMC', proficiency: 4 },
            { name: 'PyTorch', proficiency: 3 }
          ]
        },
        {
          group: 'Methods',
          skills: [
            { name: 'Time-series forecasting', proficiency: 5 },
            { name: 'A/B testing', proficiency: 4 },
            { name: 'Cohort and churn analysis', proficiency: 5 },
            { name: 'Customer segmentation', proficiency: 5 }
          ]
        },
        {
          group: 'Tools & Platforms',
          skills: [
            { name: 'Microsoft Fabric / Power BI', proficiency: 5 },
            { name: 'Apache Superset', proficiency: 4 },
            { name: 'Docker', proficiency: 4 },
            { name: 'Git', proficiency: 5 }
          ]
        }
      ],
      languagesSpoken: [
        { name: 'English', level: 'C1 · IELTS 8.0' },
        { name: 'German', level: 'B2' },
        { name: 'Russian', level: 'Native' }
      ]
    },

    experience: [
      {
        period: 'Nov 2025 – present',
        title: 'Working Student, Analytics',
        organisation: 'InnoGames',
        location: 'Hamburg, hybrid',
        type: 'Part-time',
        description: 'Testing Microsoft Fabric for analytics workflows, plus funnel and A/B-test analysis.'
      },
      {
        period: '2024–27',
        title: 'M.Sc. Management & Data Science',
        organisation: 'Leuphana University Lüneburg',
        location: null,
        type: 'Study',
        description: 'GPA 1.9 (German scale, 1.0 = best) · Deutschlandstipendium scholar · expected March 2027.'
      },
      {
        period: '2024–25',
        title: 'Data Analyst',
        organisation: 'Absolute Insurance',
        location: 'Moscow, remote',
        type: 'Full-time',
        description: 'Automated Excel-based financial reporting in Power BI for underwriting teams; MS SQL Server analysis of operational and claims data for segmentation and pricing; clustering to identify high-risk policy segments.'
      },
      {
        period: '2021',
        title: 'CFA Level I',
        organisation: 'CFA Institute',
        location: null,
        type: 'Certification',
        description: 'Passed.'
      },
      {
        period: '2019–23',
        title: 'Financial Analyst',
        organisation: 'Arkada Company',
        location: 'Moscow',
        type: 'Full-time',
        description: 'Startup launch: market-entry analysis and partner due diligence (Grenada, Turkey, UAE), competitor analysis, revenue projections.'
      },
      {
        period: '2011–19',
        title: 'Market Research Analyst',
        organisation: 'MTS PJSC',
        location: 'Moscow',
        type: 'Full-time',
        description: 'Market, competitor and trend analysis for monthly management reporting (India); telecom market analysis to identify M&A targets (Serbia, Slovenia, Moldova).'
      },
      {
        period: '2006–11',
        title: 'Corporate Affairs Associate',
        organisation: 'Agency for Property Management',
        location: 'Moscow',
        type: 'Full-time',
        description: 'Analysis of company holdings (India, Armenia, Tajikistan), documentation for mergers and divestitures.'
      },
      {
        period: '1999–05',
        title: 'Engineer-Economist, Economics & Management',
        organisation: 'RUDN University',
        location: 'Moscow',
        type: 'Study',
        description: "Graduated with Distinction · additional diploma: Translator in Professional Communication (English) · KMK statement of comparability (2023): equivalent to German Master's level."
      }
    ],

    projects: [
      {
        id: 'P-010',
        slug: 'text-informed-forecasting',
        title: 'Game revenue forecasting with two foundation models',
        description: 'Two frozen foundation forecasters, TabPFN-TS and Chronos-2, with agent-compiled planning-text covariates tested against a shuffled-text placebo, across 54 monthly origins. The held-out evaluation is pending.',
        tech: ['TabPFN-TS', 'Chronos-2', 'LLM agents', 'Time series', 'Open-weight models'],
        year: 2026
      },
      {
        id: 'P-009',
        slug: 'fuel-price-forecasting',
        title: 'Fuel price forecasting with TabPFN-3.5 and LLM event features',
        description: 'Tested whether LLM-extracted event features from EIA’s weekly petroleum narrative improve TabPFN-3.5 gasoline price forecasts on a frozen 2016 to 2024 holdout, with a placebo that shuffles content but keeps timing.',
        tech: ['TabPFN-3.5', 'LLM extraction', 'Time series', 'Placebo test'],
        year: 2026
      },
      {
        id: 'P-008',
        slug: 'tabpfn-vs-pareto-nbd',
        title: 'TabPFN-3.5 vs Bayesian Pareto/NBD customer models',
        description: 'Benchmarked when TabPFN-3.5 beats Pareto/NBD and Abe (2009) hierarchical Bayes at predicting 90-day customer return and purchase counts, on frozen holdout origins with customer-clustered bootstrap intervals and learning curves.',
        tech: ['TabPFN-3.5', 'Pareto/NBD', 'Hierarchical Bayes', 'LightGBM'],
        year: 2026
      },
      {
        id: 'P-007',
        slug: null,
        title: 'One-off multi-agent LLM toolkit',
        description: 'Built a one-off multi-agent LLM toolkit (MCP) to speed up reporting work.',
        tech: ['MCP', 'Multi-Agent', 'LLM', 'Microsoft Fabric / Power BI'],
        year: 2026
      },
      {
        id: 'P-006',
        slug: null,
        externalUrl: 'https://chef-treff.de/hackathon/',
        title: 'ChefTreff AI Hackathon: Founder Assistant',
        description: 'Multi-agent assistant that helps founders launch a company in Germany, covering business plan, marketing plan, and legal documentation. Hackathon, Hamburg.',
        tech: ['Multi-Agent', 'LLM'],
        year: 2026
      },
      {
        id: 'P-005',
        slug: 'knowledge-graph-question-answering',
        title: 'Knowledge Graph Question Answering with LLMs',
        description: 'SPARQL-based question answering over structured knowledge graphs, translating natural language questions into executable graph queries over RDF knowledge bases.',
        tech: ['SPARQL', 'RDF', 'NLP', 'Knowledge Graphs'],
        year: 2026
      },
      {
        id: 'P-004',
        slug: 'kvg-school-bus-routing',
        title: 'Lüneburg Public Bus Routing with HVV Timetable Data',
        description: 'Applied machine learning pipeline to model and predict local bus routes for regional transport operator KVG, fusing public transport geospatial data with predictive models.',
        tech: ['ML', 'Geospatial', 'Forecasting', 'Open Data'],
        year: 2026
      },
      {
        id: 'P-003',
        slug: 'artist-influence-networks',
        title: 'Artist influence networks with Neo4j',
        description: 'Graph database analysis using Neo4j and Cypher to investigate musical lineage, community clustering, and quantitative influence centrality across artists.',
        tech: ['Neo4j', 'Cypher', 'Graph Analytics'],
        year: 2025
      },
      {
        id: 'P-002',
        slug: 'bayesian-pareto-nbd',
        title: 'Hierarchical Bayesian Pareto/NBD customer modelling',
        description: 'Implemented and validated the hierarchical Bayesian Pareto/NBD model from Abe (2009) on the canonical CDNOW dataset using MCMC sampling in PyMC.',
        tech: ['PyMC', 'MCMC', 'Bayesian Statistics', 'CLV'],
        year: 2025
      },
      {
        id: 'P-001',
        slug: 'construction-defect-detection',
        title: 'Broken-tile detection with YOLOv8',
        description: 'Built in 24 hours: a computer vision object detection and classification pipeline for identifying broken, chipped, or damaged roofing materials from product imagery.',
        tech: ['PyTorch', 'CNN', 'Computer Vision', 'YOLOv8'],
        year: 2025
      }
    ],

    hiring: {
      rolesOpenTo: 'Data Scientist or Data Analyst positions involving LLM-based systems, automated forecasts, or analytics platforms',
      sectorFit: [
        'Insurance and reinsurance analytics',
        'Gaming and consumer products',
        'AI-native startups and applied AI labs working on LLM systems, agent architectures, and retrieval',
        'Telecommunications and network analytics',
        'Global technology firms and platform teams in Munich, Hamburg, Düsseldorf, and Berlin',
        'Startups and scale-ups where production ML and agent systems form the core product'
      ],
      availability: 'From April 2027',
      employmentType: 'Full-time',
      country: 'Germany',
      preferredLocations: ['Munich', 'Hamburg', 'Düsseldorf', 'Berlin'],
      howToApply: 'Contact by email (timsalakhetdinov@gmail.com) or LinkedIn (linkedin.com/in/timursalakhetdinov); typical response time is within 24 hours.',
      contact: {
        email: 'timsalakhetdinov@gmail.com',
        linkedin: 'https://www.linkedin.com/in/timursalakhetdinov'
      },
      cvUrl: CV_URL,
      cvUrlDe: CV_URL_DE
    },

    contact: {
      email: 'timsalakhetdinov@gmail.com',
      linkedin: 'https://www.linkedin.com/in/timursalakhetdinov',
      github: 'https://github.com/TimurSalakhetdinov',
      medium: 'https://medium.com/@timursalakhetdinov',
      website: SITE_URL,
      cvUrl: CV_URL,
      cvUrlDe: CV_URL_DE
    }
  };

  function textResult(data) {
    return { content: [{ type: 'text', text: JSON.stringify(data) }] };
  }

  function safeRegister(tool) {
    try {
      var result = mc.registerTool(tool);
      if (result && typeof result.catch === 'function') {
        result.catch(function (err) {
          if (window.console && typeof console.debug === 'function') {
            console.debug('webmcp: tool registration failed for ' + tool.name, err);
          }
        });
      }
    } catch (err) {
      if (window.console && typeof console.debug === 'function') {
        console.debug('webmcp: tool registration threw for ' + tool.name, err);
      }
    }
  }

  function projectUrl(slug, language) {
    var suffix = language === 'de' ? '-de.html' : '.html';
    return SITE_URL + 'projects/' + slug + suffix;
  }

  safeRegister({
    name: 'get_profile',
    description: 'Get a quick overview of who Timur Salakhetdinov is: name, headline, summary, current role, education, availability, location, spoken languages, the site URL, and links to his CV (PDF, English) and German CV/Lebenslauf (PDF). Use this first when an AI agent, recruiter, or potential collaborator wants a general introduction to Timur before looking at his skills, experience, or projects.',
    inputSchema: { type: 'object', properties: {} },
    annotations: { readOnlyHint: true },
    execute: function () {
      return textResult(DATA.profile);
    }
  });

  safeRegister({
    name: 'get_skills',
    description: "Get Timur Salakhetdinov's technical skills, grouped exactly as shown on the site (Languages, LLM & Agents, ML & Forecasting, Methods, Tools & Platforms), each with a self-assessed proficiency from 1 to 5, plus spoken languages. Use this when a recruiter or hiring agent needs to check whether his skill set matches a role, or a potential collaborator wants to assess technical fit for a project.",
    inputSchema: { type: 'object', properties: {} },
    annotations: { readOnlyHint: true },
    execute: function () {
      return textResult(DATA.skills);
    }
  });

  safeRegister({
    name: 'get_experience',
    description: "Get Timur Salakhetdinov's work history and education in reverse-chronological-ish order as listed on the site, including organisation, title, dates, location, type, and a short description for each role or degree. Use this when a recruiter, hiring agent, or ATS/CV-screening tool is building a candidate profile, or when anyone wants to understand his career background in analytics and data science.",
    inputSchema: { type: 'object', properties: {} },
    annotations: { readOnlyHint: true },
    execute: function () {
      return textResult({ experience: DATA.experience });
    }
  });

  safeRegister({
    name: 'list_projects',
    description: "List Timur Salakhetdinov's selected projects and research (LLM agent systems, foundation model forecasting, Bayesian modelling, knowledge graphs, and computer vision), each with a title, short description, tech/tags, year, and a URL to the project page. Optionally pass {query} to filter by a keyword matched against the title, description, or tech (e.g. 'TabPFN', 'LLM', 'Bayesian', 'Neo4j'), and optionally pass {language: 'de'} to get German project page URLs instead of English. Use this when a collaborator is looking for relevant work to team up on, a recruiter wants evidence of applied skills, or an agent is asked 'what has Timur built'.",
    inputSchema: {
      type: 'object',
      properties: {
        query: {
          type: 'string',
          description: "Optional keyword to filter projects by title, description, or tech/tags (case-insensitive substring match), e.g. 'TabPFN' or 'Bayesian'."
        },
        language: {
          type: 'string',
          enum: ['en', 'de'],
          description: "Optional language for the returned project URLs. Defaults to 'en'."
        }
      }
    },
    annotations: { readOnlyHint: true },
    execute: function (input) {
      var params = input || {};
      var language = params.language === 'de' ? 'de' : 'en';
      var query = typeof params.query === 'string' ? params.query.trim().toLowerCase() : '';

      var projects = DATA.projects.filter(function (project) {
        if (!query) {
          return true;
        }
        var haystack = (
          project.title + ' ' + project.description + ' ' + project.tech.join(' ')
        ).toLowerCase();
        return haystack.indexOf(query) !== -1;
      }).map(function (project) {
        return {
          id: project.id,
          title: project.title,
          description: project.description,
          tech: project.tech,
          year: project.year,
          url: project.slug ? projectUrl(project.slug, language) : (project.externalUrl || null)
        };
      });

      return textResult({ projects: projects });
    }
  });

  safeRegister({
    name: 'get_hiring_info',
    description: "Find out what kind of roles Timur Salakhetdinov is open to, his availability/start date, preferred locations, employment type, the sectors his experience fits best, how to contact or apply, and links to his CV (PDF, English) and German CV/Lebenslauf (PDF). Use this when a recruiter, hiring manager, or hiring bot wants to know whether and how to reach out to him about a job opportunity.",
    inputSchema: { type: 'object', properties: {} },
    annotations: { readOnlyHint: true },
    execute: function () {
      return textResult(DATA.hiring);
    }
  });

  safeRegister({
    name: 'get_contact',
    description: "Get Timur Salakhetdinov's professional contact channels: email, LinkedIn, GitHub, Medium, his website, and links to his CV (PDF, English) and German CV/Lebenslauf (PDF). Use this when an agent, recruiter, or collaborator needs a direct way to reach him.",
    inputSchema: { type: 'object', properties: {} },
    annotations: { readOnlyHint: true },
    execute: function () {
      return textResult(DATA.contact);
    }
  });
})();
