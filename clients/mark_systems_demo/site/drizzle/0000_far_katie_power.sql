CREATE TYPE "public"."agent_id" AS ENUM('lab-director', 'devops', 'ui-generator', 'content-curator', 'docs-writer', 'business-strategist', 'showroom-publisher', 'deploy-sentinel');--> statement-breakpoint
CREATE TYPE "public"."run_status" AS ENUM('pending', 'running', 'success', 'error', 'partial');--> statement-breakpoint
CREATE TABLE "agent_calls" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"run_id" uuid NOT NULL,
	"agent_id" "agent_id" NOT NULL,
	"step_order" integer NOT NULL,
	"input" text NOT NULL,
	"output" text,
	"error" text,
	"model" text NOT NULL,
	"provider" text NOT NULL,
	"tokens_used" integer DEFAULT 0 NOT NULL,
	"cost_usd" numeric(10, 6) DEFAULT '0' NOT NULL,
	"duration_ms" integer DEFAULT 0 NOT NULL,
	"soic_score" numeric(3, 1),
	"created_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "runs" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"user_id" uuid,
	"objective" text NOT NULL,
	"plan" jsonb NOT NULL,
	"status" "run_status" DEFAULT 'pending' NOT NULL,
	"total_cost_usd" numeric(10, 4) DEFAULT '0' NOT NULL,
	"total_tokens_used" integer DEFAULT 0 NOT NULL,
	"started_at" timestamp DEFAULT now() NOT NULL,
	"completed_at" timestamp
);
--> statement-breakpoint
CREATE TABLE "users" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"email" text,
	"name" text,
	"image" text,
	"email_verified" timestamp,
	"quota_usd_remaining" numeric(10, 4) DEFAULT '5.0000' NOT NULL,
	"quota_reset_at" timestamp,
	"created_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "users_email_unique" UNIQUE("email")
);
--> statement-breakpoint
ALTER TABLE "agent_calls" ADD CONSTRAINT "agent_calls_run_id_runs_id_fk" FOREIGN KEY ("run_id") REFERENCES "public"."runs"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "runs" ADD CONSTRAINT "runs_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "agent_calls_run_idx" ON "agent_calls" USING btree ("run_id");--> statement-breakpoint
CREATE INDEX "agent_calls_agent_idx" ON "agent_calls" USING btree ("agent_id");--> statement-breakpoint
CREATE INDEX "runs_user_idx" ON "runs" USING btree ("user_id");--> statement-breakpoint
CREATE INDEX "runs_status_idx" ON "runs" USING btree ("status");--> statement-breakpoint
CREATE INDEX "runs_started_at_idx" ON "runs" USING btree ("started_at");--> statement-breakpoint
CREATE INDEX "users_email_idx" ON "users" USING btree ("email");
