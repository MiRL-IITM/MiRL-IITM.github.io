import { defineCollection, reference } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// People Collection - Team members (faculty, students, alumni)
const people = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/people' }),
  schema: ({ image }) =>
    z.object({
      name: z.string(),
      firstName: z.string(),
      lastName: z.string(),
      role: z.enum([
        'faculty',
        'postdoc',
        'phd',
        'masters',
        'undergraduate',
        'visiting',
        'staff',
        'alumni',
      ]),
      title: z.string(),
      photo: image(),
      email: z.string().email().optional(),
      website: z.string().url().optional(),
      googleScholar: z.string().url().optional(),
      orcid: z.string().optional(),
      linkedin: z.string().url().optional(),
      twitter: z.string().optional(),
      github: z.string().optional(),
      researchInterests: z.array(z.string()).optional(),
      currentPosition: z.string().optional(),
      currentAffiliation: z.string().optional(),
      thesisTitle: z.string().optional(),
      graduationYear: z.number().optional(),
      startDate: z.coerce.date().optional(),
      endDate: z.coerce.date().optional(),
      order: z.number().optional(),
      featured: z.boolean().default(false),
      draft: z.boolean().default(false),
    }),
});

// Projects Collection - Research projects
const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      shortTitle: z.string().optional(),
      description: z.string(),
      status: z.enum(['active', 'completed', 'upcoming']),
      startDate: z.coerce.date(),
      endDate: z.coerce.date().optional(),
      topics: z.array(z.string()),
      featuredImage: image().optional(),
      investigators: z.array(z.string()), // Person IDs
      funding: z
        .array(
          z.object({
            agency: z.string(),
            grantNumber: z.string().optional(),
          })
        )
        .optional(),
      collaborators: z.array(z.string()).optional(),
      featured: z.boolean().default(false),
      order: z.number().optional(),
      draft: z.boolean().default(false),
    }),
});

// Publications Collection - Academic papers
const publications = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/publications' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      authors: z.array(z.string()),
      venue: z.string(),
      venueShort: z.string().optional(),
      year: z.number(),
      month: z.number().min(1).max(12).optional(),
      volume: z.string().optional(),
      issue: z.string().optional(),
      pages: z.string().optional(),
      doi: z.string().optional(),
      arxiv: z.string().optional(),
      pmid: z.string().optional(),
      pdfUrl: z.string().url().optional(),
      projectUrl: z.string().url().optional(),
      codeUrl: z.string().url().optional(),
      dataUrl: z.string().url().optional(),
      type: z.enum([
        'journal',
        'conference',
        'workshop',
        'preprint',
        'thesis',
        'book-chapter',
        'patent',
      ]),
      topics: z.array(z.string()),
      thumbnail: image().optional(),
      labAuthors: z.array(z.string()).optional(), // Person IDs
      award: z.string().optional(),
      featured: z.boolean().default(false),
      bibtex: z.string().optional(),
      draft: z.boolean().default(false),
    }),
});

// Posts Collection - Blog/News
const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      description: z.string(),
      pubDate: z.coerce.date(),
      updatedDate: z.coerce.date().optional(),
      category: z.enum([
        'research-highlight',
        'publication',
        'award',
        'event',
        'announcement',
        'tutorial',
      ]),
      tags: z.array(z.string()).optional(),
      heroImage: image().optional(),
      heroImageAlt: z.string().optional(),
      author: z.string().optional(), // Person ID
      featured: z.boolean().default(false),
      draft: z.boolean().default(false),
    }),
});

// Courses Collection
const courses = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/courses' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      courseNumber: z.string(),
      description: z.string(),
      semester: z.enum(['fall', 'spring', 'summer']),
      year: z.number(),
      schedule: z.string().optional(),
      location: z.string().optional(),
      instructors: z.array(z.string()), // Person IDs
      credits: z.number().optional(),
      level: z.enum(['undergraduate', 'graduate', 'mixed']),
      prerequisites: z.array(z.string()).optional(),
      syllabusUrl: z.string().url().optional(),
      courseWebsite: z.string().url().optional(),
      thumbnail: image().optional(),
      currentlyOffered: z.boolean().default(true),
      draft: z.boolean().default(false),
      semesterDates: z.string().optional(),
      communication: z.string().optional(),
      lectureMode: z.string().optional(),
    }),
});

export const collections = {
  people,
  projects,
  publications,
  posts,
  courses,
};
